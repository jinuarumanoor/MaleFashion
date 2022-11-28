from django.urls import path

from .import views


urlpatterns = [
    
    path('', views.admin_login, name='adminlogin'),
    path('active_users',views.active_users,name='active_users'),
    path('adminlogout', views.admin_logout, name='adminlogout'),
    path('adminhome',views.admin_home,name='adminhome'),

     # User block
    path("activeusers", views.active_users, name="activeusers"),
    path("blockuser/<user_id>", views.block_user, name="blockuser"),
    path("unblockuser/<user_id>", views.unblock_user, name="unblockuser"),
    path("deleteuser/<user_id>", views.delete_user, name="deleteuser"),

     # Category
    path('admincategory', views.category_list, name='categorylist'),
    path('addadmincategory', views.add_category, name='addcategory'),
    path('editcategory/<int:id>', views.edit_category, name='edit-category'),
    path('deletecategory/<int:id>', views.delete_category, name='delete-category'),

     # Variation
    path("variation", views.variation, name="variation"),
    path('addvariation', views.add_variation, name='addvariation'),
    path("deletevariation/<int:id>", views.delete_variation, name="deletevariation"),

     # Coupon
    path("viewcoupon", views.view_coupon, name="viewcoupon"),
    path('addadmincoupon', views.add_coupon, name='addcoupon'),
    path('deletecoupon/<int:id>', views.delete_coupon, name='delete-coupon'),

    #product
    path('productlist', views.product_list, name='product_list'),  
    path('addadminproduct', views.add_product, name='addproduct'),
    path('deleteproduct/<int:id>', views.delete_product, name='delete-product'),
    path('editproduct/<int:id>', views.edit_product, name='edit-product'),


    # Brand
    path('adminbrand', views.brand_list, name='brandlist'),
    path('addadminbrand', views.add_brand, name='addbrand'),
    path('deletebrand/<int:id>', views.delete_brand, name='delete-brand'),
    path('editbrand/<int:id>', views.edit_brand, name='edit-brand'),

      # Order
    path("orderdisplay/", views.order_display, name="orderdisplay"),
    path('orderdetailsadmin/<int:id>/', views.order_details_admin, name='orderdetailsadmin'),
    path('orderstatus/<int:id>/', views.order_status, name='orderstatus'),



    # Category Offer
    path('category_offer', views.category_offer, name='category_offer'),
    path('add_category_offer', views.add_category_offer, name='add_category_offer'),
    path("blockCategoryOffer/<category_id>", views.block_category_offer, name="blockCategoryOffer"),
    path("unblockCategoryOffer/<category_id>", views.unblock_category_offer, name="unblockCategoryOffer"),
    path("deleteCategoryOffer/<category_id>", views.delete_category_offer, name="deleteCategoryOffer"),
    path("editCategoryOffer/<category_id>", views.edit_category_offer, name="editCategoryOffer"),

    # Product Offer
    path('product_offer', views.product_offer, name='product_offer'),
    path('add_product_offer', views.add_product_offer, name='add_product_offer'),
    path("blockProductOffer/<product_id>", views.block_product_offer, name="blockProductOffer"),
    path("unblockProductOffer/<product_id>", views.unblock_product_offer, name="unblockProductOffer"),
    path("deleteProductOffer/<product_id>", views.delete_product_offer, name="deleteProductOffer"),
    path("editProductOffer/<product_id>", views.edit_product_offer, name="editProductOffer"),    

        # Sales Report
    path('sales_report', views.sales_report, name='sales_report'),
    path("sales_export_csv", views.sales_export_csv, name="sales_export_csv"),
    path("sales_export_pdf", views.sales_export_pdf, name="sales_export_pdf"),

]