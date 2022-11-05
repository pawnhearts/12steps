# Generated by Django 4.1.3 on 2022-11-05 20:22

from django.db import migrations


def add_feelings(*args):
    from guide.models import Feeling
    feelings = ['злость',
                'гнев',
                'возмущение',
                'ненависть',
                'обида',
                'сердитость',
                'досада',
                'раздражение',
                'мстительность',
                'оскорбленность',
                'воинственность',
                'бунтарство',
                'сопротивление',
                'зависть',
                'надменность',
                'неповиновение',
                'презрение',
                'отвращение',
                'подавленность',
                'уязвленность',
                'подозрительность',
                'циничность',
                'настороженность',
                'озабоченность',
                'тревожность',
                'страх',
                'нервозность',
                'трепет',
                'обеспокоенность',
                'испуг',
                'тревога',
                'волнение',
                'стресс',
                'боязнь',
                'ужас',
                'подверженность навязчивой идее',
                'ощущение угрозы',
                'ошеломленность',
                'опасение',
                'уныние',
                'ощущение тупика',
                'запутанность',
                'потерянность',
                'дезориентация',
                'бессвязность',
                'ощущение ловушки',
                'одиночество',
                'изолированность',
                'грусть',
                'печаль',
                'горе',
                'угнетенность',
                'мрачность',
                'отчаяние',
                'депрессия',
                'опустошенность',
                'беспомощность',
                'слабость',
                'ранимость',
                'угрюмость',
                'серьезность',
                'подавленность',
                'разочарование',
                'боль',
                'отсталость',
                'застенчивость',
                'чувство отсутствия к вам любви',
                'покинутость',
                'болезненность',
                'нелюдимость',
                'удрученность',
                'усталость',
                'глупость',
                'апатия',
                'самодовольство',
                'скука',
                'истощение',
                'расстройство',
                'упадок сил',
                'сварливость',
                'нетерпеливость',
                'вспыльчивость',
                'тоска',
                'хандра',
                'стыд',
                'вина',
                'униженность',
                'ущемленность',
                'смущение',
                'неудобство',
                'тяжесть',
                'сожаление',
                'укоры совести',
                'рефлексия',
                'скорбь',
                'отчужденность',
                'неловкость',
                'удивление',
                'шок',
                'поражение',
                'остолбенение',
                'изумление',
                'потрясение',
                'впечатлительность',
                'сильное желание',
                'энтузиазм',
                'взволнованность',
                'возбужденность',
                'страсть',
                'помешательство',
                'эйфория',
                'трепет',
                'дух соперничества',
                'твердая уверенность',
                'решимость',
                'уверенность в себе',
                'дерзость',
                'готовность',
                'оптимизм',
                'удовлетворенность',
                'гордость',
                'сентиментальность',
                'счастье',
                'радость',
                'блаженство',
                'забавность',
                'восхищение',
                'триумф',
                'удачливость',
                'удовольствие',
                'безобидность',
                'мечтательность',
                'очарование',
                'оцененность по достоинству',
                'признательность',
                'надежда',
                'заинтересованность',
                'увлеченность',
                'интерес',
                'оживленность',
                'живость',
                'спокойствие',
                'удовлетворенность',
                'облегчение',
                'мирность',
                'расслабленность',
                'довольство',
                'комфорт',
                'сдержанность',
                'восприимчивость',
                'прощение',
                'любовь',
                'безмятежность',
                'расположение',
                'обожание',
                'восхищение',
                'благоговение',
                'любовь',
                'привязанность',
                'безопасность',
                'уважение',
                'дружелюбие',
                'симпатия',
                'сочувствие',
                'нежность',
                'великодушие',
                'одухотворенность',
                'озадаченность',
                'смятение']
    for feeling in feelings:
        Feeling.objects.get_or_create(title=feeling)


class Migration(migrations.Migration):
    dependencies = [
        ("guide", "0002_alter_question_options_alter_section_options_and_more"),
    ]

    operations = [
        migrations.RunPython(add_feelings),
    ]
