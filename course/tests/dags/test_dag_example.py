import os
import logging
from contextlib import contextmanager
import pytest # type: ignore
from airflow.models import DagBag


APPROVED_TAGS = {}

@contextmanager
def suppress_logging(namespace):
    logger = logging.getLogger(namespace)
    old_value = logger.disabled
    logger.disabled = True

    try:
        yield
    finally:
        logger.disabled = old_value


def get_import_errors():
    with suppress_logging('airflow'):
        dag_bag = DagBag(include_examples=False)

        def strip_path_prefix(path):
            return os.path.relpath(path, os.environ.get('AIRFLOW_HOME'))

        return [(None, None)] + [
            (strip_path_prefix(k), v.strip()) for k, v in dag_bag.import_errors.items()
        ]


def get_dags():
    with suppress_logging('airflow'):
        dag_bag = DagBag(include_examples=False)

        def strip_path_prefix(path):
            return os.path.relpath(path, os.environ.get('AIRFLOW_HOME'))

        return [(k, v, strip_path_prefix(v.fileloc)) for k, v in dag_bag.dags.items()]


@pytest.mark.parametrize(
    'rel_path,rv', get_import_errors(), ids=[x[0] for x in get_import_errors()]
)
def test_file_imports(rel_path, rv):
    if rel_path and rv:
        raise Exception(f"{rel_path} failed to import with message \n {rv}")


@pytest.mark.parametrize(
    'dag_id,dag,fileloc', get_dags(), ids=[x[0] for x in get_dags()]
)
def test_dag_tags(dag_id, dag, fileloc):
    assert dag.tags, f"{dag_id} in {fileloc} has no tags"
    if APPROVED_TAGS:
        assert not set(dag.tags) - APPROVED_TAGS


@pytest.mark.parametrize(
    'dag_id,dag,fileloc', get_dags(), ids=[x[0] for x in get_dags()]
)
def test_dag_retries(dag_id, dag, fileloc):
    assert (
        dag.default_args.get('retries', None) >= 2
    ), f"{dag_id} in {fileloc} must have task retries >= 2."