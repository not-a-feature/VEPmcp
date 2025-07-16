import pytest
from vep_mcp.bridge import VEPValidator


def test_validate_species():
    assert VEPValidator.validate_species("homo_sapiens") == "homo_sapiens"
    assert VEPValidator.validate_species("Homo Sapiens") == "homo_sapiens"
    with pytest.raises(ValueError):
        VEPValidator.validate_species("")
    with pytest.raises(ValueError):
        VEPValidator.validate_species("homo sapiens!")


def test_validate_hgvs_notation():
    assert (
        VEPValidator.validate_hgvs_notation("ENST00000366667:c.803C>T")
        == "ENST00000366667:c.803C>T"
    )
    with pytest.raises(ValueError):
        VEPValidator.validate_hgvs_notation("")


def test_validate_variant_id():
    assert VEPValidator.validate_variant_id("rs12345") == "rs12345"
    with pytest.raises(ValueError):
        VEPValidator.validate_variant_id("")


def test_validate_genomic_region():
    # Valid formats
    assert VEPValidator.validate_genomic_region("1:230710048:A/G") == "1:230710048:A/G"
    assert VEPValidator.validate_genomic_region("1:230710048") == "1:230710048"
    assert VEPValidator.validate_genomic_region("1:230710048-230710049") == "1:230710048-230710049"
    assert VEPValidator.validate_genomic_region("9:22125503-22125502:1") == "9:22125503-22125502:1"
    assert VEPValidator.validate_genomic_region("X:100000-100100:1") == "X:100000-100100:1"
    assert VEPValidator.validate_genomic_region("1:1-100:A/G") == "1:1-100:A/G"
    assert (
        VEPValidator.validate_genomic_region("9:22125503-22125502:1/C") == "9:22125503-22125502:1/C"
    )
    assert (
        VEPValidator.validate_genomic_region("21:26960070-26960071/G") == "21:26960070-26960071/G"
    )

    # Invalid formats
    with pytest.raises(ValueError):
        VEPValidator.validate_genomic_region("invalid:format")
    with pytest.raises(ValueError):
        VEPValidator.validate_genomic_region("")


def test_validate_batch_size():
    assert VEPValidator.validate_batch_size(["a", "b"]) == ["a", "b"]
    with pytest.raises(ValueError):
        VEPValidator.validate_batch_size([])
    with pytest.raises(ValueError):
        VEPValidator.validate_batch_size(["a"] * 1001)
