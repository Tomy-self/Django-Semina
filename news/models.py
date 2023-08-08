from django.db import models

class Reporter(models.Model):
    full_name = models.CharField(max_length=70)
    rid = models.CharField(max_length=20, default='sejin')

    def __str__(self):
        return self.full_name
    


class Article(models.Model):
    ARTICLE_CATEGORIES = (('VOICE','Voice'), ('STORY','Story'), ('MUSIC','Music'), ('TEXT','Text'), ('EXTRA', 'Extra'))
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    head_image = models.ImageField(upload_to='news/img/%Y/%m/%d',blank=True)
    content = models.TextField()
    file_content = models.FileField(upload_to='news/files/%Y/%m/%d', blank=True)
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    article_category = models.CharField(max_length=5, choices=ARTICLE_CATEGORIES, default='VOICE')

    def __str__(self):
        return self.headline
    
    def get_absolute_url(self):
        return f'news/{self.pk}'