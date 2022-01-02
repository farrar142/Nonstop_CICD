from django.test import TestCase
from .models import *

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #UserDataCreate
        for id in range(1, 4):
            username = f"user{id}"
            password = f"user{id}"
            first_name = f"이름{id}"
            last_name = f"성{id}"
            email = f"test{id}@test.com"
            gender = 'M'
            User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name,email=email, gender=gender)
        #MarketDataCreate
        Market(name="언니네옷가게", site_url="https://www.abc1.co.kr", email="test1@test.com", master_id=1).save()
        Market(name="누나네옷가게", site_url="https://www.abc2.co.kr", email="test2@test.com", master_id=2).save()
        Market(name="이모네옷가게", site_url="https://www.abc3.co.kr", email="test3@test.com", master_id=3).save()
        #ProductDataCreate
        product = Product(market_id=1, name="원피스1", display_name="인스타여신원피스1", price=10000, sale_price=9000)
        product.save()
        #ProductRealDataCreate
        ProductReal(product=product, option_1_name="44", option_1_display_name="44", option_2_name="RED",
                option_2_display_name="감성레드").save()

    def test_First_name_label(self):
        author = User.objects.get(id=3)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label,'이름')#ko-kr = '이름' en-us = 'first_name'

    def test_Market_name_label(self):
        market = Market.objects.get(id=3)
        field_label = market._meta.get_field('site_url').verbose_name
        self.assertEquals(field_label,'마켓사이트URL')

    def test_Product_Type_Test(self):
        product = Product.objects.get(id=1)
        price = product.price
        self.assertEquals(type(price),int)
        
    def test_Product_Real_Type_Test(self):
        productreal = ProductReal.objects.get(id=1)
        name = productreal.option_1_display_name
        self.assertEquals(type(name),str)