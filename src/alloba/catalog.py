"""Bundled supplier catalog: load, filter, search, compare."""

import json
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from re import compile as re_compile

CATEGORIES = (
    "construction",
    "machinery",
    "agro",
    "textiles",
    "electronics",
    "chemicals",
    "food_beverage",
    "automotive",
    "healthcare",
)

REGIONS = ("africa", "asia", "europe", "americas", "middle_east", "oceania")

_CATEGORY_ALIASES = {
    "food_beverage": {"food", "food & beverage", "f&b", "beverage", "agri-food", "agrifood"},
    "construction": {"building", "construction materials"},
    "machinery": {"machine", "equipment", "industrial"},
    "agro": {"agriculture", "farming", "agri"},
    "textiles": {"textile", "clothing", "fabric"},
    "electronics": {"electronic", "electrical"},
    "chemicals": {"chemical"},
    "automotive": {"auto", "vehicles", "parts"},
    "healthcare": {"health", "medical", "pharma"},
}

_REGION_ALIASES = {
    "africa": {"african", "west africa", "east africa", "south africa"},
    "asia": {"asian", "south east asia", "china", "india"},
    "europe": {"european", "eu"},
    "americas": {"north america", "south america", "usa", "latin america"},
    "middle_east": {"gulf", "uae", "saudi"},
    "oceania": {"australia", "pacific"},
}


@dataclass
class CatalogProduct:
    id: int
    name: str
    name_l10n: dict
    cat: str
    region: str
    spec: str
    spec_l10n: dict
    supplier: str
    location: str
    price: str
    unit: str
    rating: float
    reviews: int
    lead_time: str
    moq: str
    thumb: str

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "name_l10n": self.name_l10n,
            "cat": self.cat,
            "region": self.region,
            "spec": self.spec,
            "spec_l10n": self.spec_l10n,
            "supplier": self.supplier,
            "location": self.location,
            "price": self.price,
            "unit": self.unit,
            "rating": self.rating,
            "reviews": self.reviews,
            "leadTime": self.lead_time,
            "moq": self.moq,
            "thumb": self.thumb,
        }


class Catalog:
    """In-memory index over the catalog shipped with the package."""

    def __init__(self, path: str | None = None) -> None:
        raw = self._load(path)
        self.products = [_product(item) for item in raw]
        self._by_id = {p.id: p for p in self.products}
        self._tokens: dict[str, set[int]] = {}
        for p in self.products:
            for token in (
                self._tokenize(p.name) | self._tokenize(p.spec) | self._tokenize(p.supplier)
            ):
                self._tokens.setdefault(token, set()).add(p.id)

    @staticmethod
    def _load(path: str | None) -> list[dict]:
        if path:
            return json.loads(Path(path).read_text(encoding="utf-8"))
        bundled = files("alloba").joinpath("data", "products.json")
        return json.loads(bundled.read_text(encoding="utf-8"))

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return {t for t in re_compile(r"[a-z0-9]+").findall(text.lower()) if len(t) > 1}

    @property
    def size(self) -> int:
        return len(self.products)

    def all_products(self) -> list[dict]:
        return [p.as_dict() for p in self.products]

    def get(self, product_id: int) -> dict | None:
        p = self._by_id.get(product_id)
        return p.as_dict() if p else None

    def search(
        self,
        query: str,
        category: str | None = None,
        region: str | None = None,
        max_results: int = 10,
    ) -> list[dict]:
        cat = self._normalize_alias(category, _CATEGORY_ALIASES)
        reg = self._normalize_alias(region, _REGION_ALIASES)
        scored: list[tuple[float, CatalogProduct]] = []
        tokens = self._tokenize(query)
        for p in self.products:
            if cat and p.cat != cat:
                continue
            if reg and p.region != reg:
                continue
            score = 0.0
            if not tokens:
                score = 1.0
            else:
                for token in tokens:
                    score += self._match_score(p, token)
                score = score / len(tokens)
            if score > 0:
                scored.append((score, p))
        scored.sort(key=lambda pair: (-pair[0], -pair[1].rating))
        return [
            {**p.as_dict(), "score": round(score, 4)}
            for score, p in scored[: max(1, min(max_results, len(scored)))]
        ]

    @staticmethod
    def _match_score(p: CatalogProduct, token: str) -> float:
        fields = ((p.name, 3.0), (p.spec, 1.5), (p.supplier, 1.5), (p.cat, 1.0), (p.region, 1.0))
        for value, weight in fields:
            if token in value.lower() or value.lower().find(token) >= 0:
                return weight
            if value.lower().startswith(token):
                return weight * 0.9
        return 0.0

    @staticmethod
    def _normalize_alias(value: str | None, aliases: dict[str, set[str]]) -> str | None:
        if not value:
            return None
        candidate = value.strip().lower()
        for canonical, names in aliases.items():
            if candidate in names or candidate == canonical:
                return canonical
        return candidate

    def compare(self, product_ids: list[int]) -> dict:
        products = [self.get(pid) for pid in product_ids if self.get(pid) is not None]
        return {
            "fields": [
                "name",
                "category",
                "region",
                "supplier",
                "location",
                "price",
                "unit",
                "rating",
                "lead_time",
                "moq",
            ],
            "products": products,
        }


def _product(item: dict) -> CatalogProduct:
    return CatalogProduct(
        id=int(item["id"]),
        name=item["name"],
        name_l10n=item.get("name_l10n", {}),
        cat=item["cat"],
        region=item["region"],
        spec=item.get("spec", ""),
        spec_l10n=item.get("spec_l10n", {}),
        supplier=item.get("supplier", ""),
        location=item.get("location", ""),
        price=item.get("price", ""),
        unit=item.get("unit", ""),
        rating=float(item.get("rating", 0.0)),
        reviews=int(item.get("reviews", 0)),
        lead_time=item.get("leadTime", ""),
        moq=item.get("moq", ""),
        thumb=item.get("thumb", ""),
    )


catalog = Catalog()
