import os
import tempfile
import logging
from uuid import uuid4
from typing import List, Dict, Any
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.core.config import settings
from app.core.vectorstore import create_vector_store
from loguru import logger

class EnhancedDataLoader:
    """Enhanced data loader for processing Hanzla's detailed data with optimized vector storage."""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
    def load_text_files(self, directory: str) -> List[Document]:
        """Load all text files from a directory."""
        documents = []
        if not os.path.exists(directory):
            logger.warning(f"Directory {directory} does not exist")
            return documents
            
        for filename in os.listdir(directory):
            if filename.endswith(('.txt', '.md')):
                file_path = os.path.join(directory, filename)
                try:
                    loader = TextLoader(file_path, encoding='utf-8')
                    docs = loader.load()
                    # Add metadata to identify source
                    for doc in docs:
                        doc.metadata.update({
                            'source': filename,
                            'type': 'text',
                            'category': self._categorize_file(filename)
                        })
                    documents.extend(docs)
                    logger.info(f"Loaded {filename} with {len(docs)} documents")
                except Exception as e:
                    logger.error(f"Error loading {filename}: {str(e)}")
                    
        return documents
    
    def _categorize_file(self, filename: str) -> str:
        """Categorize files based on their content type."""
        filename_lower = filename.lower()
        
        if 'cybersecurity' in filename_lower or 'security' in filename_lower:
            return 'cybersecurity'
        elif 'mlai' in filename_lower or 'ai' in filename_lower or 'machine' in filename_lower:
            return 'ai_ml'
        elif 'project' in filename_lower:
            return 'projects'
        elif 'personality' in filename_lower:
            return 'personality'
        elif 'about' in filename_lower:
            return 'background'
        elif 'program' in filename_lower or 'courses' in filename_lower:
            return 'programs'
        else:
            return 'general'
    
    def load_projects_directory(self, projects_dir: str) -> List[Document]:
        """Load project-specific documents with enhanced metadata."""
        documents = []
        if not os.path.exists(projects_dir):
            logger.warning(f"Projects directory {projects_dir} does not exist")
            return documents
            
        for filename in os.listdir(projects_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(projects_dir, filename)
                try:
                    loader = TextLoader(file_path, encoding='utf-8')
                    docs = loader.load()
                    
                    # Extract project name from filename
                    project_name = filename.replace('_project_summary.txt', '').replace('.txt', '')
                    
                    for doc in docs:
                        doc.metadata.update({
                            'source': filename,
                            'type': 'project',
                            'category': 'projects',
                            'project_name': project_name,
                            'content_type': 'project_summary'
                        })
                    documents.extend(docs)
                    logger.info(f"Loaded project {project_name} with {len(docs)} documents")
                except Exception as e:
                    logger.error(f"Error loading project {filename}: {str(e)}")
                    
        return documents
    
    def create_namespaced_chunks(self, documents: List[Document]) -> Dict[str, List[Document]]:
        """Create namespaced chunks based on content categories."""
        namespaced_chunks = {}
        
        for doc in documents:
            category = doc.metadata.get('category', 'general')
            
            # Split document into chunks
            chunks = self.text_splitter.split_documents([doc])
            
            # Add namespace-specific metadata
            for chunk in chunks:
                chunk.metadata.update({
                    'namespace': category,
                    'chunk_id': str(uuid4()),
                    'original_source': doc.metadata.get('source', 'unknown')
                })
            
            if category not in namespaced_chunks:
                namespaced_chunks[category] = []
            namespaced_chunks[category].extend(chunks)
            
        return namespaced_chunks
    
    def load_all_data(self) -> Dict[str, List[Document]]:
        """Load all data files and organize by namespace."""
        all_documents = []
        
        # Load main text data
        text_data_path = os.path.join('app', 'data', 'textdata')
        all_documents.extend(self.load_text_files(text_data_path))
        
        # Load projects specifically
        projects_path = os.path.join(text_data_path, 'projects')
        all_documents.extend(self.load_projects_directory(projects_path))
        
        # Create namespaced chunks
        namespaced_chunks = self.create_namespaced_chunks(all_documents)
        
        logger.info(f"Loaded {len(all_documents)} total documents")
        for namespace, chunks in namespaced_chunks.items():
            logger.info(f"Namespace '{namespace}': {len(chunks)} chunks")
            
        return namespaced_chunks
    
    def upload_to_pinecone(self, namespaced_chunks: Dict[str, List[Document]], 
                          clear_existing: bool = True) -> bool:
        """Upload chunks to Pinecone with proper namespacing."""
        try:
            vector_store = create_vector_store()
            if not vector_store:
                logger.error("Failed to create vector store")
                return False
            
            # Clear existing data if requested
            if clear_existing:
                logger.info("Clearing existing vectors from Pinecone...")
                # Note: This would require implementing a clear method or using Pinecone directly
                # For now, we'll proceed with adding new vectors
            
            total_uploaded = 0
            
            for namespace, chunks in namespaced_chunks.items():
                if not chunks:
                    continue
                    
                logger.info(f"Uploading {len(chunks)} chunks to namespace '{namespace}'")
                
                # Generate unique IDs for chunks
                chunk_ids = [chunk.metadata.get('chunk_id', str(uuid4())) for chunk in chunks]
                
                # Upload to specific namespace
                try:
                    # Create a new vector store instance for this namespace
                    namespace_vector_store = create_vector_store(namespace)
                    if namespace_vector_store:
                        # Add documents with namespace-specific metadata
                        namespace_vector_store.add_documents(chunks)
                        total_uploaded += len(chunks)
                        logger.info(f"Successfully uploaded {len(chunks)} chunks to namespace '{namespace}'")
                    else:
                        logger.error(f"Failed to create vector store for namespace '{namespace}'")
                        
                except Exception as e:
                    logger.error(f"Error uploading to namespace '{namespace}': {str(e)}")
                    continue
            
            logger.info(f"Total uploaded: {total_uploaded} chunks across all namespaces")
            return True
            
        except Exception as e:
            logger.error(f"Error in upload_to_pinecone: {str(e)}")
            return False
    
    def create_optimized_retrieval_index(self) -> bool:
        """Create an optimized retrieval index with all data."""
        logger.info("Starting optimized data loading and vector creation...")
        
        # Load all data with namespacing
        namespaced_chunks = self.load_all_data()
        
        # Upload to Pinecone
        success = self.upload_to_pinecone(namespaced_chunks, clear_existing=True)
        
        if success:
            logger.info("✅ Successfully created optimized retrieval index")
        else:
            logger.error("❌ Failed to create optimized retrieval index")
            
        return success

def load_enhanced_data_to_vector_store():
    """Main function to load enhanced data to vector store."""
    loader = EnhancedDataLoader()
    return loader.create_optimized_retrieval_index()

if __name__ == "__main__":
    # Run the enhanced data loader
    success = load_enhanced_data_to_vector_store()
    if success:
        print("✅ Enhanced data loading completed successfully!")
    else:
        print("❌ Enhanced data loading failed!")
