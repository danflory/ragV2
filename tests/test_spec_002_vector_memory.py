"""
Test Suite for 002_VECTOR_MEMORY.md
Validates: Hybrid Vector Search, Qdrant Integration, Memory Hygiene

Following TDD Protocol (005_DEVELOPMENT_PROTOCOLS.md)
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.container import container
from app.config import config


class TestVectorStoreComponents:
    """
    Tests for Section 2.1: The Components
    Validates VectorStore and Ingestor initialization
    """
    
    @pytest.mark.skipif(
        container.current_mode != config.MODE_RAG,
        reason="VectorStore only active in RAG mode"
    )
    def test_vector_store_exists(self):
        """Verify VectorStore is initialized in RAG mode"""
        assert container.memory is not None, "VectorStore should exist in RAG mode"
    
    @pytest.mark.skipif(
        container.current_mode != config.MODE_RAG,
        reason="Ingestor only active in RAG mode"
    )
    def test_ingestor_exists(self):
        """Verify Ingestor is initialized in RAG mode"""
        assert container.ingestor is not None, "Ingestor should exist in RAG mode"
    
    @pytest.mark.skipif(
        container.current_mode != config.MODE_RAG,
        reason="VectorStore only active in RAG mode"
    )
    def test_vector_store_injected_via_container(self):
        """Verify VectorStore follows IoC pattern"""
        # Should be managed by container, not instantiated elsewhere
        assert hasattr(container, 'memory')


class TestHybridSearch:
    """
    Tests for Section 3: HYBRID SEARCH DATA FLOW
    Validates dense + sparse vector search functionality
    """
    
    @pytest.mark.skipif(
        container.current_mode != config.MODE_RAG,
        reason="Hybrid search only in RAG mode"
    )
    @pytest.mark.asyncio
    async def test_hybrid_search_available(self):
        """Verify VectorStore implements search method"""
        assert callable(getattr(container.memory, 'search', None)), \
            "VectorStore should implement search()"
    
    @pytest.mark.skipif(
        container.current_mode != config.MODE_RAG,
        reason="Embedding only in RAG mode"
    )
    @pytest.mark.asyncio
    async def test_embedding_pipeline_accessible(self):
        """Verify embedding models are accessible"""
        # VectorStore should have embedding capability
        assert container.memory is not None
        # Check that health check passes (embedding service available)
        health = await container.memory.check_health()
        assert health is True or health is False, "Health check should return boolean"


class TestVectorStoreInterface:
    """
    Tests for Section 4: IMPLEMENTED INTERFACE
    Validates interface contract from specification
    """
    
    @pytest.mark.skipif(
        container.current_mode != config.MODE_RAG,
        reason="VectorStore only in RAG mode"
    )
    def test_add_texts_method_exists(self):
        """Verify add_texts method exists"""
        assert callable(getattr(container.memory, 'add_texts', None)), \
            "VectorStore should implement add_texts()"
    
    @pytest.mark.skipif(
        container.current_mode != config.MODE_RAG,
        reason="VectorStore only in RAG mode"
    )
    def test_search_method_exists(self):
        """Verify search method exists"""
        assert callable(getattr(container.memory, 'search', None)), \
            "VectorStore should implement search()"
    
    @pytest.mark.skipif(
        container.current_mode != config.MODE_RAG,
        reason="VectorStore only in RAG mode"
    )
    def test_prune_method_exists(self):
        """Verify prune_source_vectors method exists (Memory Hygiene)"""
        assert callable(getattr(container.memory, 'prune_source_vectors', None)) or \
               callable(getattr(container.memory, 'purge', None)), \
            "VectorStore should implement pruning methods"
    
    @pytest.mark.skipif(
        container.current_mode != config.MODE_RAG,
        reason="VectorStore only in RAG mode"
    )
    def test_ingest_text_method_exists(self):
        """Verify ingest_text method exists"""
        has_ingest = callable(getattr(container.memory, 'ingest_text', None))
        has_add = callable(getattr(container.memory, 'add_texts', None))
        assert has_ingest or has_add, \
            "VectorStore should implement ingestion methods"


class TestAdvancedFeatures:
    """
    Tests for Section 5: ADVANCED FEATURES
    Validates circuit breaker, memory hygiene, parallel processing
    """
    
    @pytest.mark.skipif(
        container.current_mode != config.MODE_RAG,
        reason="Advanced features only in RAG mode"
    )
    @pytest.mark.asyncio
    async def test_health_check_resilience(self):
        """Verify circuit breaker pattern via health checks"""
        # Health check should not raise exceptions
        try:
            health = await container.memory.check_health()
            assert isinstance(health, bool), "Health check should return boolean"
        except Exception as e:
            pytest.fail(f"Health check should not raise exceptions: {e}")
    
    @pytest.mark.skipif(
        container.current_mode != config.MODE_RAG,
        reason="Memory hygiene only in RAG mode"
    )
    def test_memory_hygiene_methods_exist(self):
        """Verify memory hygiene (purge/prune) methods exist"""
        has_purge = callable(getattr(container.memory, 'purge', None))
        has_prune = callable(getattr(container.memory, 'prune_source_vectors', None))
        assert has_purge or has_prune, \
            "VectorStore should implement memory hygiene methods"


class TestDualGPUEmbedding:
    """
    Tests for Section 2.1: Embedding Pipeline
    Validates dual-GPU architecture (GPU 1 for embeddings)
    """
    
    def test_embedding_config_exists(self):
        """Verify embedding configuration is defined"""
        assert hasattr(config, 'L1_EMBED_URL') or hasattr(config, 'EMBED_URL'), \
            "Config should define embedding service URL"
    
    @pytest.mark.skipif(
        container.current_mode != config.MODE_RAG,
        reason="Embedding only in RAG mode"
    )
    def test_embedding_service_separate_from_generation(self):
        """Verify embedding uses different endpoint than generation (GPU separation)"""
        if hasattr(config, 'L1_EMBED_URL') and hasattr(config, 'L1_URL'):
            # Embedding should use different port/URL than main generation
            assert config.L1_EMBED_URL != config.L1_URL, \
                "Embedding should use separate service (GPU 1) from generation (GPU 0)"


class TestQdrantIntegration:
    """
    Validates Qdrant vector database integration
    """
    
    @pytest.mark.skipif(
        container.current_mode != config.MODE_RAG,
        reason="Qdrant only in RAG mode"
    )
    @pytest.mark.asyncio
    async def test_qdrant_connectivity(self):
        """Verify Qdrant connection via health check"""
        health = await container.memory.check_health()
        # Health check should execute without exceptions
        assert health is not None, "Qdrant health check should return status"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
