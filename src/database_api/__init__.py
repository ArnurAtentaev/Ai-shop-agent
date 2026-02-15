from fastapi import APIRouter

from .products.views import router_product
from .shop.views import router_shop
from .answers_to_questions.views import router_question

router = APIRouter()
router.include_router(router=router_product)
router.include_router(router=router_shop, prefix="/shop")
router.include_router(router=router_question, prefix="/question")
