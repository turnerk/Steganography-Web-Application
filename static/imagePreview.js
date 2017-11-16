// $('#orig').change(function(e) {
//     changed = true;
//     loadImage('orig', drawImagePreview);
//     // $('#cover-preset').val('na');
// });

// var changed = true;

// function downloadCanvas(link, canvas, filename) {
//     link.href = canvas.toDataURL();
//     link.download=filename;
// }

// var factor = {
//     "orig": 0.001,
//     "secret": 0.001,
// };
// var k = 0.001;
// var opposite = {
//     "orig": "secret",
//     "secret": "orig",
// };

// var loaded_img = {
//     "orig": undefined,
//     "secret": undefined,
//     "stegimage": undefined,
// };

// function loadImage(which, cb) {
//     var input = $('#' + which)[0];

//     loaded_img[which] = undefined;

//     var img = new Image;
//     img.onload = function() {
//         loaded_img[which] = img;
//         cb(which);
//     }
//     img.src = URL.createObjectURL(input.files[0]);
// }


// function drawImagePreview(which, recursed) {
//     var id = '#' + which + 'canvas';

//     var ctx = $(id)[0].getContext('2d');

//     var targetw = $(id)[0].width;
//     var targeth = $(id)[0].height;

//     var img = loaded_img[which];
//     var imgw = img.width;
//     var imgh = img.height;
//     var wfactor = img.width / targetw;
//     var hfactor = img.height / targeth;
//     factor[which] = wfactor;
//     if (hfactor > factor[which])
//         factor[which] = hfactor;

//     k = factor[which];
//     if (factor[opposite[which]] > factor[which])
//         k = factor[opposite[which]];

//     // draw the image to the canvas
//     ctx.clearRect(0, 0, targetw, targeth);
//     ctx.drawImage(img, 0, 0, imgw / k, imgh / k);

//     if (loaded_img[opposite[which]]) {
//         if (!recursed) {
//             drawImagePreview(opposite[which], 1);
//         } else {
//             makeHideImagePreview($('#bits').slider('value'));
//         }
//     }
// }
function imagePrev(){
    var canvas = document.getElementById('origcanvas');
    var context = canvas.getContext('2d');
    var imageObj = new Image();

    imageObj.onload = function() {
    context.drawImage(imageObj, 0, 0, imageObj.width, imageObj.height, 0, 0, canvas.width, canvas.height);
    };
    imageObj.src = 'https://stega.me/uploads/128146147110.png';
};