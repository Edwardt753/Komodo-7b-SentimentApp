import re

def clean_comment(comment):
    # Menghapus @user
    comment = re.sub(r'@+[\w]+', '', comment)
    
    # Hapus symbol dan karakter lain
    comment = re.sub(r'[^\w\s]', '', comment)
    comment = re.sub(r'\s+', ' ', comment).strip()
    
    # Lowercase
    comment = comment.lower()
    
    # Do not remove stopwords
    cleaned_comment = comment
    
    return cleaned_comment

def clean_comments_list(comments_list):
    return [clean_comment(comment) for comment in comments_list]
