from django.db import models

# جدول تعريف الألعاب
class Game(models.Model):
    title = models.CharField(max_length=100, verbose_name="اسم اللعبة")
    category = models.CharField(max_length=50, verbose_name="التصنيف")
    description = models.TextField(verbose_name="الوصف")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# جدول تسجيل نتائج وجولات اللعب
class GameScore(models.Model):
    player_name = models.CharField(max_length=50, verbose_name="اسم اللاعب", default="Player")
    game_name = models.CharField(max_length=100, verbose_name="اللعبة")
    result = models.CharField(max_length=100, verbose_name="النتيجة")
    played_at = models.DateTimeField(auto_now_add=True, verbose_name="وقت اللعب")

    def __str__(self):
        return f"{self.player_name} - {self.game_name} ({self.result})"