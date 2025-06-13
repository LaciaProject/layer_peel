"""
Layer Peel Utility Functions Module

Provides auxiliary functions for file processing, encoding detection, MIME type recognition, etc.
"""

from typing import Iterator, Generator, Any, Optional
from io import BytesIO
import mimetypes
import chardet
from contextlib import contextmanager
import magic
import logging

from .types import RawIOBase
from .exceptions import EncodingError, FileAccessError

# Setup logging
logger = logging.getLogger(__name__)


def read_stream(file: RawIOBase, size: int = 65536) -> Iterator[bytes]:
    """
    Read data from file object in chunks

    Args:
        file: File object implementing RawIOBase protocol
        size: Chunk size for each read, default 64KB

    Yields:
        bytes: Read data chunks

    Raises:
        FileAccessError: File read failed

    Example:
        >>> with open('file.bin', 'rb') as f:
        ...     for chunk in read_stream(f):
        ...         process_chunk(chunk)
    """
    try:
        while True:
            chunk = file.read(size)
            if not chunk:
                break
            yield chunk
    except Exception as e:
        raise FileAccessError(
            file_path=getattr(file, "name", "<unknown>"),
            operation="read",
            original_error=e,
        ) from e


def get_mime_type(data: bytes) -> str:
    """
    Detect MIME type of data

    Args:
        data: Byte data to detect

    Returns:
        str: Detected MIME type

    Raises:
        ValueError: Cannot detect MIME type

    Example:
        >>> data = b'PK\x03\x04'  # ZIP file header
        >>> mime_type = get_mime_type(data)
        >>> print(mime_type)  # 'application/zip'
    """
    if not data:
        return "application/octet-stream"

    try:
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(data)
        logger.debug(f"Detected MIME type: {mime_type}")
        return mime_type
    except Exception as e:
        logger.warning(f"MIME type detection failed: {e}")
        return "application/octet-stream"


def get_extension(mime_type: str) -> Optional[str]:
    """
    Get file extension based on MIME type

    Args:
        mime_type: MIME type string

    Returns:
        Optional[str]: Corresponding file extension, None if cannot be determined

    Example:
        >>> ext = get_extension('application/zip')
        >>> print(ext)  # '.zip'
    """
    try:
        extension = mimetypes.guess_extension(mime_type)
        if extension:
            logger.debug(f"MIME type {mime_type} corresponds to extension: {extension}")
        return extension
    except Exception as e:
        logger.warning(f"Cannot get extension for {mime_type}: {e}")
        return None


def file_to_bytesio(f: RawIOBase) -> BytesIO:
    """
    Convert file object to BytesIO object

    Args:
        f: Input file object

    Returns:
        BytesIO: BytesIO object containing file content

    Raises:
        FileAccessError: File read failed

    Example:
        >>> with open('file.bin', 'rb') as f:
        ...     bio = file_to_bytesio(f)
        ...     # Now can randomly access data in bio
    """
    try:
        content = f.read()
        return BytesIO(content)
    except Exception as e:
        raise FileAccessError(
            file_path=getattr(f, "name", "<unknown>"),
            operation="convert to BytesIO",
            original_error=e,
        ) from e


def fill_stream(
    data: Optional[Iterator[bytes]] = None, fill: Optional[bytes] = None
) -> Generator[bytes, Any, None]:
    """
    Create a data stream that outputs fill data first, then iterator data

    Args:
        data: Optional byte iterator
        fill: Optional fill byte data

    Yields:
        bytes: Data chunks

    Example:
        >>> header = b'header_data'
        >>> stream = iter([b'chunk1', b'chunk2'])
        >>> for chunk in fill_stream(stream, header):
        ...     print(chunk)
        # Output: b'header_data', b'chunk1', b'chunk2'
    """
    if fill is not None:
        yield fill
    if data is not None:
        try:
            yield from data
        except Exception as e:
            logger.warning(f"Data stream read error: {e}")


def fix_encoding(file_name: bytes) -> str:
    """
    Fix filename encoding issues

    Attempts to automatically detect the encoding of byte sequence and convert to string.
    If detection fails, uses error ignore mode for decoding.

    Args:
        file_name: Original filename in byte form

    Returns:
        str: Decoded filename string

    Raises:
        EncodingError: Encoding processing failed

    Example:
        >>> raw_name = b'\xe4\xb8\xad\xe6\x96\x87.txt'  # UTF-8 encoded "中文.txt"
        >>> decoded = fix_encoding(raw_name)
        >>> print(decoded)  # '中文.txt'
    """
    if not file_name:
        return ""

    try:
        # First try to detect encoding
        detected = chardet.detect(file_name)
        detected_encoding = detected.get("encoding")
        confidence = detected.get("confidence", 0)

        logger.debug(
            f"Detected encoding: {detected_encoding} (confidence: {confidence})"
        )

        if detected_encoding and confidence > 0.7:
            try:
                return file_name.decode(detected_encoding)
            except (UnicodeDecodeError, LookupError) as e:
                logger.warning(
                    f"Decoding with detected encoding {detected_encoding} failed: {e}"
                )

        # Try common encodings
        for encoding in ["utf-8", "gbk", "gb2312", "latin1"]:
            try:
                return file_name.decode(encoding)
            except (UnicodeDecodeError, LookupError):
                continue

        # Finally use error ignore mode
        result = file_name.decode("utf-8", errors="ignore")
        if result:
            logger.warning(
                f"Decoded filename using ignore error mode: {file_name!r} -> {result!r}"
            )
            return result

        # If still fails, return hex representation
        hex_name = file_name.hex()
        logger.warning(f"Cannot decode filename, using hex: {hex_name}")
        return f"unknown_{hex_name}"

    except Exception as e:
        raise EncodingError(file_name, original_error=e) from e


@contextmanager
def lifespan(path: str):
    """
    Lifespan manager for tracking extraction progress

    Args:
        path: File path being processed

    Yields:
        None

    Example:
        >>> with lifespan("archive.zip"):
        ...     # Process compressed file
        ...     pass
    """
    logger.info(f"Starting extraction: {path}")
    try:
        yield
    except Exception as e:
        logger.error(f"Extraction failed: {path} - {e}")
        raise
    finally:
        logger.info(f"Completed extraction: {path}")
