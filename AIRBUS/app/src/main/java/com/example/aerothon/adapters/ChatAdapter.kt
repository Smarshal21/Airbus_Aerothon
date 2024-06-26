package com.example.aerothon.adapters

import android.content.Context
import android.content.Intent
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.aerothon.R
import com.example.aerothon.databinding.AirlinesChatUserItemLayoutBinding
import com.example.aerothon.models.UserModel

class ChatAdapter(var context: Context, var list:ArrayList<UserModel>) : RecyclerView.Adapter<ChatAdapter.ChatViewHolder>() {

    inner class ChatViewHolder(view: View) : RecyclerView.ViewHolder(view){
        var binding : AirlinesChatUserItemLayoutBinding = AirlinesChatUserItemLayoutBinding.bind(view)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ChatViewHolder {
        return ChatViewHolder(
            LayoutInflater.from(parent.context)
            .inflate(R.layout.Airlines_chat_user_item_layout,parent,false))
    }

    override fun getItemCount(): Int {
        return list.size
    }

    override fun onBindViewHolder(holder: ChatViewHolder, position: Int) {
        val user = list[position]
        //set the profile
        //Glide.with(context).load(user.imageUrl).into(holder.binding.userImage)
        holder.binding.userName.text = user.name
        holder.binding.userId.text = user.uid
        holder.binding.userEmail.text = user.email

        //on click
        holder.itemView.setOnClickListener {
            val intent = Intent(context,AirlinesChatScreenActivity::class.java)
            intent.putExtra("uid",user.uid)
            context.startActivity(intent)
        }

    }
}