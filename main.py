from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, List, Optional


@dataclass(frozen=True)
class CoffeeOrder:
    base: str
    size: str
    milk: str
    syrups: Tuple[str, ...]
    sugar: int
    iced: bool
    price: float
    description: str

    def __str__(self) -> str:
        if self.description:
            return self.description
        return f"{self.size} {self.base} ({self.price:.2f})"


class CoffeeOrderBuilder:

    BASE_PRICES = {
        "espresso": 200.0,
        "americano": 250.0,
        "latte": 300.0,
        "cappuccino": 320.0,
    }

    SIZE_MULTIPLIERS = {
        "small": 1.0,
        "medium": 1.2,
        "large": 1.4,
    }

    MILK_PRICES = {
        "none": 0.0,
        "whole": 30.0,
        "skim": 30.0,
        "oat": 60.0,
        "soy": 50.0,
    }

    SYRUP_PRICE = 40.0
    ICED_RATE = 0.2
    MAX_SUGAR = 5
    MAX_SYRUPS = 4

    ALLOWED_BASES = tuple(BASE_PRICES.keys())
    ALLOWED_SIZES = tuple(SIZE_MULTIPLIERS.keys())
    ALLOWED_MILKS = tuple(MILK_PRICES.keys())

    def __init__(self) -> None:
        self._base: Optional[str] = None
        self._size: Optional[str] = None
        self._milk: str = "none"
        self._syrups: List[str] = []
        self._sugar: int = 0
        self._iced: bool = False

    def set_base(self, base: str) -> "CoffeeOrderBuilder":
        if base not in self.ALLOWED_BASES:
            raise ValueError(f"base должен быть одним из {self.ALLOWED_BASES}")
        self._base = base
        return self

    def set_size(self, size: str) -> "CoffeeOrderBuilder":
        if size not in self.ALLOWED_SIZES:
            raise ValueError(f"size должен быть одним из {self.ALLOWED_SIZES}")
        self._size = size
        return self

    def set_milk(self, milk: str) -> "CoffeeOrderBuilder":
        if milk not in self.ALLOWED_MILKS:
            raise ValueError(f"milk должен быть одним из {self.ALLOWED_MILKS}")
        self._milk = milk
        return self

    def add_syrup(self, syrup_name: str) -> "CoffeeOrderBuilder":
        name = syrup_name.strip().lower()
        if not name:
            raise ValueError("Название сиропа не может быть пустым")
        if name in self._syrups:
            return self
        if len(self._syrups) >= self.MAX_SYRUPS:
            raise ValueError(f"Максимум {self.MAX_SYRUPS} сиропов на напиток")
        self._syrups.append(name)
        return self

    def set_sugar(self, teaspoons: int) -> "CoffeeOrderBuilder":
        if not isinstance(teaspoons, int):
            raise ValueError("Сахар должен быть целым числом")
        if teaspoons < 0 or teaspoons > self.MAX_SUGAR:
            raise ValueError(f"Сахар должен быть в диапазоне 0..{self.MAX_SUGAR}")
        self._sugar = teaspoons
        return self

    def set_iced(self, iced: bool = True) -> "CoffeeOrderBuilder":
        self._iced = iced
        return self

    def clear_extras(self) -> "CoffeeOrderBuilder":
        """Сбросить молоко, сиропы, сахар и лёд."""
        self._milk = "none"
        self._syrups = []
        self._sugar = 0
        self._iced = False
        return self

    def build(self) -> CoffeeOrder:
        if self._base is None:
            raise ValueError("Не задан base")
        if self._size is None:
            raise ValueError("Не задан size")
        base = self._base
        size = self._size
        milk = self._milk
        syrups_tuple: Tuple[str, ...] = tuple(self._syrups)
        sugar = self._sugar
        iced = self._iced
        price = self._calc_price(
            base=base,
            size=size,
            milk=milk,
            syrups_count=len(syrups_tuple),
            iced=iced,
        )
        description = self._make_description(
            base=base,
            size=size,
            milk=milk,
            syrups=syrups_tuple,
            sugar=sugar,
            iced=iced,
        )
        return CoffeeOrder(
            base=base,
            size=size,
            milk=milk,
            syrups=syrups_tuple,
            sugar=sugar,
            iced=iced,
            price=price,
            description=description,
        )

    def _calc_price(
        self,
        base: str,
        size: str,
        milk: str,
        syrups_count: int,
        iced: bool,
    ) -> float:
        base_price = self.BASE_PRICES[base]
        size_coef = self.SIZE_MULTIPLIERS[size]
        milk_extra = self.MILK_PRICES[milk]
        syrups_extra = self.SYRUP_PRICE * syrups_count
        iced_extra = base_price * self.ICED_RATE if iced else 0.0
        total = base_price * size_coef + milk_extra + syrups_extra + iced_extra
        return float(total)

    def _make_description(
        self,
        base: str,
        size: str,
        milk: str,
        syrups: Tuple[str, ...],
        sugar: int,
        iced: bool,
    ) -> str:
        parts: List[str] = []
        parts.append(f"{size} {base}")
        if milk != "none":
            parts.append(f"with {milk} milk")
        if syrups:
            parts.append("+ " + ", ".join(syrups) + " syrup")
        if iced:
            parts.append("(iced)")
        if sugar > 0:
            unit = "tsp" if sugar == 1 else "tsps"
            parts.append(f"{sugar} {unit} sugar")

        return " ".join(parts)

def _run_tests() -> None:
    builder = CoffeeOrderBuilder()
    basic_order = (
        builder
        .set_base("latte")
        .set_size("medium")
        .set_milk("oat")
        .add_syrup("vanilla")
        .set_sugar(2)
        .set_iced(True)
        .build()
    )

    assert isinstance(basic_order, CoffeeOrder)
    assert isinstance(basic_order.price, float)
    assert basic_order.price > 0
    assert basic_order.base == "latte"
    assert basic_order.size == "medium"
    assert basic_order.milk == "oat"
    assert "vanilla" in basic_order.syrups
    assert basic_order.sugar == 2
    assert basic_order.iced is True
    assert str(basic_order)

    first_order_builder = CoffeeOrderBuilder()
    first_order = (
        first_order_builder
        .set_base("espresso")
        .set_size("small")
        .set_sugar(1)
        .build()
    )

    second_order_builder = CoffeeOrderBuilder()
    second_order = (
        second_order_builder
        .set_base("espresso")
        .set_size("small")
        .set_sugar(1)
        .add_syrup("caramel")
        .build()
    )

    assert first_order.base == "espresso"
    assert first_order.size == "small"
    assert first_order.sugar == 1
    assert first_order.syrups == ()
    assert second_order.syrups == ("caramel",)
    assert second_order.price > first_order.price
    assert first_order.syrups == ()
    assert first_order.price != 0.0

    b = CoffeeOrderBuilder()
    try:
        b.set_size("small").build()
        raise AssertionError("Ожидали ValueError, если base не задан")
    except ValueError:
        pass

    b = CoffeeOrderBuilder()
    try:
        b.set_base("latte").build()
        raise AssertionError("Ожидали ValueError, если size не задан")
    except ValueError:
        pass

    b = CoffeeOrderBuilder().set_base("latte").set_size("small")
    try:
        b.set_sugar(10)
        raise AssertionError("Ожидали ValueError при сахаре > 5")
    except ValueError:
        pass
    try:
        b.set_sugar(-1)
        raise AssertionError("Ожидали ValueError при сахаре < 0")
    except ValueError:
        pass

    b = CoffeeOrderBuilder().set_base("americano").set_size("large")
    b.add_syrup("vanilla").add_syrup("caramel").add_syrup("hazelnut").add_syrup("chocolate")
    order_with_syrups = b.add_syrup("vanilla").build()
    assert len(order_with_syrups.syrups) == 4

    try:
        (
            CoffeeOrderBuilder()
            .set_base("americano")
            .set_size("large")
            .add_syrup("1")
            .add_syrup("2")
            .add_syrup("3")
            .add_syrup("4")
            .add_syrup("5")
        )
        raise AssertionError("Ожидали ValueError при попытке добавить >4 сиропов")
    except ValueError:
        pass

    hot_espresso = CoffeeOrderBuilder().set_base("espresso").set_size("small").build()
    iced_espresso = (
        CoffeeOrderBuilder()
        .set_base("espresso")
        .set_size("small")
        .set_iced(True)
        .build()
    )
    assert iced_espresso.price > hot_espresso.price
    print("All inline tests passed.")

if __name__ == "__main__":
    _run_tests()
