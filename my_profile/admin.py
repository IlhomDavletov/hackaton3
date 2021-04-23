from django.contrib import admin

from my_profile.models import Profile, CodeImage, Review


# admin.site.register(Profile)

class CodeImageInline(admin.TabularInline):
    model = CodeImage
    min_num = 1
    max_num = 10

@admin.register(Profile)
class ProblemAdmin(admin.ModelAdmin):
    inlines = [CodeImageInline,]

# class ReviewInline(admin.TabularInline):
#     model = Review
#
# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     inlines = [ReviewInline,]
#     list_filter = ('created',)