"""
测试核心解压缩功能
"""

import pytest
from io import BytesIO
from unittest.mock import Mock, patch

from layer_peel import extract
from layer_peel.exceptions import MaxDepthExceededError, ExtractionError


class TestExtract:
    """测试 extract 函数"""

    def test_extract_with_zero_depth(self):
        """测试深度为0时的行为"""
        data = BytesIO(b"test data")

        with pytest.raises(MaxDepthExceededError):
            list(extract(data, "test.txt", depth=0))

    def test_extract_empty_data(self):
        """测试空数据的处理"""
        data = BytesIO(b"")

        results = list(extract(data, "empty.txt", depth=1))
        assert len(results) == 1

        file_data, file_path, mime_type = results[0]
        assert file_path == "empty.txt"
        assert b"".join(file_data) == b""

    def test_extract_non_archive_data(self):
        """测试非压缩文件数据"""
        test_data = b"This is just plain text data"
        data = BytesIO(test_data)

        results = list(extract(data, "plain.txt", depth=1))
        assert len(results) == 1

        file_data, file_path, mime_type = results[0]
        assert file_path == "plain.txt"
        assert b"".join(file_data) == test_data
        assert mime_type == "text/plain"

    @patch("layer_peel.iter_unpack.get_mime_type")
    def test_extract_mime_type_detection_failure(self, mock_get_mime_type):
        """测试MIME类型检测失败的情况"""
        mock_get_mime_type.side_effect = Exception("MIME detection failed")

        test_data = b"some data"
        data = BytesIO(test_data)

        results = list(extract(data, "test.bin", depth=1))
        assert len(results) == 1

        file_data, file_path, mime_type = results[0]
        assert file_path == "test.bin"
        assert b"".join(file_data) == test_data
        # MIME类型应该为None，因为检测失败
        assert mime_type is None

    def test_extract_with_custom_chunk_size(self):
        """测试自定义块大小"""
        test_data = b"x" * 1000  # 1KB数据
        data = BytesIO(test_data)

        results = list(extract(data, "large.txt", chunk_size=100, depth=1))
        assert len(results) == 1

        file_data, file_path, mime_type = results[0]
        assert file_path == "large.txt"
        assert b"".join(file_data) == test_data

    def test_extract_with_custom_lifespan_manager(self):
        """测试自定义生命周期管理器"""
        calls = []

        def custom_lifespan(path):
            from contextlib import contextmanager

            @contextmanager
            def manager():
                calls.append(f"start:{path}")
                try:
                    yield
                finally:
                    calls.append(f"end:{path}")

            return manager()

        test_data = b"test data"
        data = BytesIO(test_data)

        results = list(
            extract(data, "test.txt", lifespan_manager=custom_lifespan, depth=1)
        )
        assert len(results) == 1

        # 验证生命周期管理器被调用
        assert "start:test.txt" in calls
        assert "end:test.txt" in calls


class TestExtractErrorHandling:
    """测试错误处理"""

    def test_extract_with_read_error(self):
        """测试读取错误的处理"""
        mock_file = Mock()
        mock_file.read.side_effect = IOError("Read failed")

        with pytest.raises(ExtractionError):
            list(extract(mock_file, "error.txt", depth=1))

    def test_extract_with_negative_depth(self):
        """测试负数深度"""
        data = BytesIO(b"test")

        with pytest.raises(MaxDepthExceededError):
            list(extract(data, "test.txt", depth=-1))


class TestExtractIntegration:
    """集成测试"""

    def test_extract_basic_workflow(self):
        """测试基本工作流程"""
        # 创建一个简单的测试数据
        test_data = b"Hello, Layer Peel!"
        data = BytesIO(test_data)

        # 执行解压缩
        results = list(extract(data, "hello.txt"))

        # 验证结果
        assert len(results) == 1
        file_data, file_path, mime_type = results[0]

        assert file_path == "hello.txt"
        assert b"".join(file_data) == test_data
        assert mime_type is not None  # 应该检测到某种MIME类型
