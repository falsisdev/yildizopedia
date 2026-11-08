import pytest
from bot.rag_engine import RAGEngine
from bot.handlers import split_telegram_message
from bot.retrieval.query_rewriter import rewrite_query_with_history
from bot.retrieval.hybrid_search import PrerequisiteGraphRetriever

@pytest.fixture(scope="module")
def rag_engine():
    return RAGEngine()

def test_frontmatter_tier_parsing(rag_engine):
    """Tier hiyerarşisinin frontmatter'dan doğru okunduğunu test eder."""
    # 1. Topluluk / Reddit dosyası Tier 4 olmalı
    res_reddit = rag_engine.search("öğrenci toplulukları reddit itiraf", top_k=2)
    assert len(res_reddit) > 0
    top_result = res_reddit[0]
    assert "Tier 4" in top_result["tier"]

    # 2. Lisans yönetmeliği Tier 1 olmalı
    res_mevzuat = rag_engine.search("lisans eğitim öğretim yönetmeliği madde", top_k=2)
    assert len(res_mevzuat) > 0
    assert any("Tier 1" in r["tier"] for r in res_mevzuat)

def test_zero_match_behavior(rag_engine):
    """Alakasız / anlamsız sorgularda sıfır eşleşme güvenliğini test eder."""
    res_empty = rag_engine.search("xyzqweasdzxcv1234567890", top_k=5)
    assert len(res_empty) == 0

def test_telegram_message_split():
    """Telegram 4096 karakter sınırına karşı bölücüyü test eder."""
    long_text = "A" * 5000
    chunks = split_telegram_message(long_text, max_length=3900)
    assert len(chunks) == 2
    assert len(chunks[0]) == 3900
    assert len(chunks[1]) == 1100

def test_query_rewriter():
    """Takip sorusunda ders kodunun geçmişten doğru çekildiğini test eder."""
    history = [
        {"role": "user", "content": "BLM2012 dersi hangi yarıyılda?"},
        {"role": "model", "content": "BLM2012 Nesneye Yönelik Programlama dersi 3. yarıyılda verilmektedir."}
    ]
    follow_up = "Peki önkoşulu var mı?"
    rewritten = rewrite_query_with_history(follow_up, history=history)
    assert "BLM2012" in rewritten
    assert "önkoşul" in rewritten

def test_prerequisite_graph():
    """Önkoşul grafından doğrudan ders çekildiğini test eder."""
    graph_retriever = PrerequisiteGraphRetriever()
    assert len(graph_retriever.graph) > 0

    ctx = graph_retriever.get_prerequisite_context("BLM2012 dersinin önkoşulu")
    assert ctx is not None
    assert "BLM2012" in ctx["title"]
    assert "Resmi Bologna" in ctx["tier"]
