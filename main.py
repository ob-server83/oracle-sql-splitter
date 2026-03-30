from oracle_sql_splitter import SQLSplitter, split_sql

__all__ = ["SQLSplitter", "split_sql"]


if __name__ == "__main__":
    from oracle_sql_splitter.cli import main
    raise SystemExit(main())
