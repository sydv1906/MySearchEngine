from datetime import datetime, timedelta, timezone

from search.trust_ranker import TrustRanker, trust_reasons


def test_authority_score_for_known_authority_domain():
    assert TrustRanker().authority_score(
        "https://docs.python.org/3/"
    ) == 1.0


def test_authority_score_for_unknown_domain():
    assert TrustRanker().authority_score(
        "https://example.com/article"
    ) == 0.5


def test_educational_domain_gets_high_score():
    assert TrustRanker().authority_score(
        "https://example.edu/research"
    ) == 0.9


def test_government_domain_gets_high_score():
    assert TrustRanker().authority_score(
        "https://example.gov/research"
    ) == 0.95


def test_trust_score_contains_expected_fields():
    result = TrustRanker().calculate("https://docs.python.org/3/")

    assert "authority" in result
    assert "freshness" in result
    assert "trust_score" in result


def test_trust_score_is_between_zero_and_one():
    result = TrustRanker().calculate("https://example.com")

    assert 0.0 <= result["trust_score"] <= 1.0


def test_freshness_score_for_recent_page():
    recent = datetime.now(timezone.utc) - timedelta(days=2)

    assert TrustRanker().freshness_score(recent) == 1.0


def test_trust_reasons_explain_high_quality_signals():
    reasons = trust_reasons(1.0, 1.0)

    assert "High-authority domain" in reasons
    assert "Recently crawled" in reasons