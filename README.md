# 1.запуск:
cd ~/coffee
uv run python main.py

# 2.тесты:
from main import CoffeeOrderBuilder
order = (CoffeeOrderBuilder()
         .set_base("latte")
         .set_size("large")
         .set_milk("oat")
         .add_syrup("caramel")
         .set_sugar(3)
         .set_iced(True)
         .build())
print(order, order.price)
