var addSticker = function(stickerID){
   currentContent  = summernote.code()
   stickerIMG = "<img scr = ' " + stickerURL(stickerID) + " '>"
   newContent = currentContent + stickerIMG
   summernote.code(newContent)   
}