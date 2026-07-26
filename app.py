from flask import Flask, render_template, request, redirect
import boto3

app = Flask(__name__)

BUCKET_NAME = "file2cloudstorage"

s3 = boto3.client("s3")


@app.route("/")
def home():
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    files = []

    if "Contents" in response:
        for obj in response["Contents"]:
            files.append(obj["Key"])

    return render_template("index.html", files=files)


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["file"]

    if file:
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)

    return redirect("/")


@app.route("/delete/<filename>")
def delete(filename):

    s3.delete_object(
        Bucket=BUCKET_NAME,
        Key=filename
    )

    return redirect("/")


@app.route("/download/<filename>")
def download(filename):

    url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": filename
        },
        ExpiresIn=3600
    )

    return redirect(url)


if __name__ == "__main__":
    app.run(debug=True)
