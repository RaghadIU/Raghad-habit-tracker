from datetime import datetime

class Habit:
    def __init__(self, name: str, frequency: str, created_at: str = None):
        """
        يمثل كلاس العادة التي يمكن للمستخدم إضافتها وتتبعها.
        :param name: اسم العادة
        :param frequency: تكرار العادة ('daily' أو 'weekly')
        :param created_at: تاريخ إنشاء العادة (افتراضيًا هو الوقت الحالي)
        """
        self.name = name
        self.frequency = frequency
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.streak = 0  # سلسلة النجاحات المتتالية

    def complete_habit(self):
        """
        يتم استدعاء هذه الدالة عند إكمال العادة، مما يزيد من سلسلة النجاحات.
        """
        self.streak += 1

    def reset_streak(self):
        """
        إعادة تعيين سلسلة النجاحات عند فشل المستخدم في إكمال العادة في الفترة المحددة.
        """
        self.streak = 0

    def __repr__(self):
        return f"Habit(name={self.name}, frequency={self.frequency}, created_at={self.created_at}, streak={self.streak})"
