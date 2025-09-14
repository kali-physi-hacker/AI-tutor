from .users import User
from .catalog import Course, Module, Lesson
from .docs import Document, DocChunk
from .chat import Chat, Message
from .quiz import Quiz, QuizItem, QuizSubmission
from .progress import Progress
from .eval import EvalRun

# Convenience namespace for deps
class users:
    get_by_id = User.get_by_id
    get_by_email = User.get_by_email

