const createImageElement = (an_image_file) => {
  const result = $('<img class="img-responsive">');
  result.attr("src", window.URL.createObjectURL(an_image_file));
  return result
}

const updateImage = (an_image_file) => {
  $("img").remove();
  const image = createImageElement(an_image_file);
  $("figure").prepend(image);
}

const isJpegImage = (a_file) => a_file.type == "image/jpeg"

const uploadImage = (a_file) => {
  if (isJpegImage(a_file)) {
    updateImage(a_file)
  } else {
    alert("Unsupported format");
  }
}

const isEmpty = (an_array) => an_array.length === 0

const handleImageUpload = (event) => {
  const { files } = event.target;
  
  if (isEmpty(files)) {
    console.log("no image to display");
  } else {
    uploadImage(files[0])
  }
}

$('form input[type="file"]').on("change", handleImageUpload);


