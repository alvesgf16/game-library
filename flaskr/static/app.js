$('form input[type="file"]').on("change", ({ target }) => {
  let { files } = target;
  if (files.length === 0) {
    console.log("no image to display");
  } else {
    if (files[0].type == "image/jpeg") {
      $("img").remove();
      let image = $('<img class="img-responsive">');
      image.attr("src", window.URL.createObjectURL(files[0]));
      $("figure").prepend(image);
    } else {
      alert("Unsupported format");
    }
  }
});
