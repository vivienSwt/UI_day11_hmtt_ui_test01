# 对象库层
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from base.app_base.base_page import BasePage, BaseHandle
from utils import DriverUtils


class IndexPage(BasePage):
    def __init__(self):
        super().__init__()
        # 频道元素对象
        self.channel_option = (By.XPATH, "//*[contains(@text, '{}')]")
        # 频道选项区域元素对象
        self.channel_area = (By.XPATH, "//*[@class='android.widget.HorizontalScrollView']")
        # 第一条文章定位方法
        self.first_aritcle = (By.XPATH, "//*[contains(@text, '评论')]")

    # 找频道元素对象
    def find_channel_option(self, option_name):
        # self.channel_option[1].format(option_name)
        # return self.find_elt(self.channel_option)
        return DriverUtils.get_app_driver().find_element(self.channel_option[0], self.channel_option[1].format(option_name))

    # 找频道选项区元素对象
    def find_channel_area(self):
        return self.find_elt(self.channel_area)

    # 找第一条文章定位方法
    def find_first_aritcle(self):
        return self.find_elt(self.first_aritcle)


# 操作层
class IndexHandle(BaseHandle):
    def __init__(self):
        self.index_page = IndexPage()

    # 选择频道
    def check_channel_option(self, channel_name):
        # 获取区域元素的所在位置
        area_element = self.index_page.find_channel_area()
        x = area_element.location["x"]
        y = area_element.location["y"]
        # 获取区域元素的大小
        w = area_element.size["width"]
        h = area_element.size["height"]
        # 计算起始按住的滑动坐标
        start_x = x + w * 0.8
        start_y = y + h * 0.5
        # 计算目标位置的坐标
        end_x = x + w * 0.2
        end_y = start_y

        while True:
            # 先获取一次界面信息
            page_old = DriverUtils.get_app_driver().page_source
            # 在当前区域中查找我们所想选择的频道元素
            try:
                # 如果能找到则点击
                self.index_page.find_channel_option(channel_name).click()
                # 退出循环
                break
            # 找不到想选择的频道元素再次滑动页面
            except Exception as e:
                DriverUtils.get_app_driver().swipe(start_x, start_y, end_x, end_y)
                # 再次获取一次界面信息和滑动前的相等
                page_new = DriverUtils.get_app_driver().page_source
                # 滑动前后页面信息相等则抛出异常没有找到目标的选项
                if page_new == page_old:
                    raise NoSuchElementException("没有找到{}的频道")

    # 点击第一条文章
    def click_first_aritcle(self):
        self.index_page.find_first_aritcle().click()


# 业务层
class IndexProxy:
    def __init__(self):
        self.index_handle = IndexHandle()

    # 根据频道查询文章的方法
    def test_qari_by_channel(self, channel_name):
        # 选择频道
        self.index_handle.check_channel_option(channel_name)
        # 点击第一条文章
        self.index_handle.click_first_aritcle()
