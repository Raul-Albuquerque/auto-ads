from .get_all_profile_ads import router as meta_router
from .get_all_ads import router as all_meta_ads_router

meta_router.include_router(all_meta_ads_router)