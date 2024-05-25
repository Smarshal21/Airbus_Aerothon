package com.example.aerothon.models

data class MessageModel(
    var message:String? = "",
    var senderId:String? = "",
    var timeStamp:Long? = 0
){
    //time stamp is not necessary
}