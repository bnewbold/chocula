import pytest
from chocula import *


@pytest.fixture
def config():
    config = ChoculaConfig.from_file(sources_dir="tests/files/")
    return config


@pytest.fixture
def issn_db():
    return IssnDatabase(issn_issnl_file_path="tests/files/ISSN-to-ISSN-L.txt")


@pytest.fixture
def database(issn_db):
    db = ChoculaDatabase(db_file=":memory:", issn_db=issn_db)
    db.init_db()
    return db


def test_all(config, database):

    for cls in ALL_CHOCULA_DIR_CLASSES:
        loader = cls(config)
        counts = loader.index_file(database)
        assert counts["total"] >= 20
        assert counts["inserted"] > 5

    for cls in ALL_CHOCULA_KBART_CLASSES:
        loader = cls(config)
        counts = loader.index_file(database)
        assert counts["total"] >= 10
        assert counts["inserted"] >= 1

    # TODO: database.load_fatcat_containers(config)
    # TODO: database.load_fatcat_stats(config)
    # TODO: database.load_homepage_status(config)
    database.summarize()
    database.export_fatcat()
    database.export_urls()
