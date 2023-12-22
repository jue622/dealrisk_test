import numpy as np

class NDimensionalArray:
    def __init__(self, shape, default_value=0):
        """
        实现基本的N维数列数据结构，底层数据采用NumPy中的ndarray。
        :param shape: 指定数组的形状
        :param default_value: 数组默认值
        """
        # 检查shape参数是否是一个整数元组，并且所有的元素都大于0
        if not isinstance(shape, tuple) or not all(isinstance(i, int) and i > 0 for i in shape):
            raise ValueError("shape必须是一个正整数元组, 并且数组中所有的元素都大于0")

        # 此处是NumPy中的ndarray数据结构
        self.data = np.full(shape, default_value)

    def __getitem__(self, indices):
        """"
        实现获取任意元素的indexing操作，通过索引访问数组的元素。
        :param indices: 索引列表
        :return: 返回对应索引的元素值
        """
        # 检查索引是否在数组的范围内
        if not isinstance(indices, tuple) or len(indices) != len(self.data.shape):
            raise ValueError("索引必须是一个长度与数组维度相同的元组")
        # if any(i >= dim for i, dim in zip(indices, self.data.shape)):
        #     raise IndexError("索引超出范围")

        return self.data[tuple(indices)]

    def __iter__(self):
        """
        实现迭代器，依次按顺序输出数组的各项值。
        """
        self._iterator = np.nditer(self.data, flags=['multi_index'], order='C')
        return self

    def __next__(self):
        """
        迭代器的__next__方法，按指定顺序遍历数组中的每个元素。
        """
        if self._iterator.finished:
            raise StopIteration
        value = self._iterator[0]
        self._iterator.iternext()
        return value

    def slice(self, *args):
        """
        实现切片操作，返回新的切片数组，保持引用而不进行深度拷贝。
        """
        sliced_data = self.data[args]
        sliced_array = NDimensionalArray(sliced_data.shape)
        sliced_array.data = sliced_data
        return sliced_array

# 测试示例
if __name__ == "__main__":
    # 创建一个3维的N维数组（3x4x5），默认值为1
    array = NDimensionalArray((3, 4, 5, 6), default_value=2)
    print("Original Array:")
    print(array.data)

    # 获取任意元素的indexing操作
    print("\nIndexing Operation:")
    print("Element at [1, 2, 3, 4]:", array[1, 2, 3, 4])  # 时间复杂度为 O(1)

    # 迭代器示例
    print("\nIterator Operation:")
    iterator = iter(array[:,:,2,:])
    for idx, element in enumerate(iterator):
        print(f"Iter[{idx}] =", element)

    # 切片操作示例
    print("\nSlice Operation:")
    sliced = array.slice(slice(None, None, 2), slice(None, None))
    print("Sliced Array:")
    print(sliced.data)
