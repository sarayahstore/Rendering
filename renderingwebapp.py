import os
import time
import shutil
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, ImageEnhance, ImageFilter

app = FastAPI()

# إنشاء مجلدات للملفات المرفوعة والنتائج
UPLOAD_DIR = "uploads"
RESULT_DIR = "results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

# دالة الرندرة والمعالجة الاحترافية (تنفذ في الخلفية)
def heavy_rendering_task(file_path: str, output_path: str, brightness: float, contrast: float):
    try:
        # محاكاة عملية رندرة أو معالجة معقدة ثقيلة
        time.sleep(3) 
        
        # فتح الصورة والبدء في الرندرة والمعالجة الاحترافية
        with Image.open(file_path) as img:
            # 1. تحسين الإضاءة والتباين
            img = ImageEnhance.Brightness(img).enhance(brightness)
            img = ImageEnhance.Contrast(img).enhance(contrast)
            
            # 2. تطبيق فلتر لزيادة حدة التفاصيل (رندرة ناعمة واحترافية)
            img = img.filter(ImageFilter.SHARPEN)
            
            # 3. حفظ النتيجة بجودة عالية جداً 100%
            img.save(output_path, quality=100, subsampling=0)
            
        print(f"Task completed successfully: {output_path}")
    except Exception as e:
        print(f"Error during rendering: {str(e)}")

# واجهة المستخدم (HTML) تظهر عند فتح رابط الموقع
@app.get("/", response_class=HTMLResponse)
async def main_page():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>منصة الرندرة الاحترافية أونلاين</title>
        <style>
            body { font-family: Tahoma, sans-serif; background-color: #1a1a1a; color: #fff; text-align: center; padding: 50px; }
            .container { max-width: 500px; margin: auto; background: #2d2d2d; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
            input, button { width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: none; box-sizing: border-box; }
            input[type="file"] { background: #3d3d3d; color: #fff; }
            button { background-color: #007bff; color: white; font-weight: bold; cursor: pointer; transition: 0.3s; }
            button:hover { background-color: #0056b3; }
            #status { margin-top: 20px; font-weight: bold; color: #ffc107; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>رندرة الصور الإحترافية 🚀</h2>
            <form id="uploadForm">
                <input type="file" id="imageFile" accept="image/*" required>
                <label>نسبة الإضاءة:</label>
                <input type="number" id="brightness" value="1.2" step="0.1" min="0">
                <label>نسبة التباين:</label>
                <input type="number" id="contrast" value="1.1" step="0.1" min="0">
                <button type="submit">ابدأ الرندرة أونلاين</button>
            </form>
            <div id="status"></div>
        </div>

        <script>
            document.getElementById('uploadForm').onsubmit = async (e) => {
                e.preventDefault();
                const statusDiv = document.getElementById('status');
                statusDiv.innerText = "جاري رفع الصورة وبدء الرندرة الحسابية...";
                
                const formData = new FormData();
                formData.append("file", document.getElementById('imageFile').files[0]);
                
                const brightness = document.getElementById('brightness').value;
                const contrast = document.getElementById('contrast').value;

                // إرسال الطلب للسيرفر لتبدأ الرندرة في الخلفية
                const response = await fetch(`/render/?brightness=${brightness}&contrast=${contrast}`, {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                if(data.status === "processing") {
                    statusDiv.innerHTML = `جاري المعالجة... <br> انتظر قليلاً ثم قم بتحديث الرابط لتحميل النتيجة من هنا: <br> <a href="/static/${data.result_filename}" target="_blank" style="color:#28a745;">[رابط الصورة المرندرة]</a>`;
                } else {
                    statusDiv.innerText = "حدث خطأ أثناء المعالجة.";
                }
            };
        </script>
    </body>
    </html>
    """

# استقبال الصورة وبدء معالجتها خلف الكواليس دون تعطيل الموقع
@app.post("/render/")
async def start_render(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...), 
    brightness: float = 1.0, 
    contrast: float = 1.0
):
    # تسمية الملفات وحفظها
    filename = file.filename
    uploaded_path = os.path.join(UPLOAD_DIR, filename)
    result_filename = f"rendered_{filename}"
    result_path = os.path.join(RESULT_DIR, result_filename)
    
    with open(uploaded_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # إضافة المهمة الثقيلة لتعمل في الخلفية (Background Task) ليبقى الموقع سريعاً
    background_tasks.add_task(heavy_rendering_task, uploaded_path, result_path, brightness, contrast)
    
    return JSONResponse(content={
        "status": "processing", 
        "message": "الرندرة تعمل في الخلفية الآن",
        "result_filename": result_filename
    })

# مشاركة مجلد النتائج ليتمكن المستخدم من تحميل الصورة منه لاحقاً
app.mount("/static", StaticFiles(directory=RESULT_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
