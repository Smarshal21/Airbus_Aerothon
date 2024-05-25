package com.example.aerothon.adapters

import android.graphics.Color
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentManager
import androidx.recyclerview.widget.RecyclerView
import com.example.aerothon.R
import com.example.aerothon.activities.HomeScreenActivity
import com.example.aerothon.models.FlightTypeModel
import com.example.aerothon.fragments.PilotFlightDetailsFragment

class FlightTypeAdapter(private val FlightTypeList:ArrayList<FlightTypeModel>, private val activity: HomeScreenActivity):
    RecyclerView.Adapter<FlightTypeAdapter.FlightTypeViewHolder>() {

    class FlightTypeViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView){
        val tvFlightType: TextView = itemView.findViewById(R.id.tvFlightType)
        val ivFlightType: ImageView = itemView.findViewById(R.id.ivFlightType)
        val layout:LinearLayout = itemView.findViewById(R.id.layout)

    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): FlightTypeViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.rv_Flight_type_item,parent,false)
        return FlightTypeViewHolder(view)
    }

    override fun getItemCount(): Int {
        return FlightTypeList.size
    }

    var index = -1
    override fun onBindViewHolder(holder: FlightTypeViewHolder, position: Int) {
        val FlightType = FlightTypeList[position]
        holder.tvFlightType.text = FlightType.FlightType
        holder.ivFlightType.setImageResource(FlightType.FlightIcon)
        holder.itemView.setOnClickListener (object:View.OnClickListener{
            override fun onClick(p0: View?) {
                val activity = p0!!.context as AppCompatActivity
                val PilotFlightDetailsFragment = PilotFlightDetailsFragment()

                //try
                val bundle = Bundle()
                bundle.putString("FlightType", FlightType.FlightType)
                PilotFlightDetailsFragment.arguments = bundle

//                activity.supportFragmentManager.beginTransaction()
//                    .replace(R.id.fragmentContainerView,PilotFlightDetailsFragment)
//                    .addToBackStack(null)
//                    .commit()

                val fragmentManager = activity.supportFragmentManager
                fragmentManager.popBackStackImmediate(null, FragmentManager.POP_BACK_STACK_INCLUSIVE)
                val transaction = fragmentManager.beginTransaction()
                transaction.replace(R.id.fragmentContainerView, PilotFlightDetailsFragment)
                transaction.commit()

                index = position
                notifyDataSetChanged()
            }

        })

        if(index == position){
            holder.tvFlightType.setTextColor(Color.BLACK)
            holder.layout.setBackgroundColor(Color.parseColor("#FDD962"))

            val color = ContextCompat.getColor(holder.itemView.context, R.color.black)
            holder.ivFlightType.setColorFilter(color)

        }
        else{
            holder.tvFlightType.setTextColor(Color.parseColor("#C6C7C9"))
            holder.layout.setBackgroundColor(Color.parseColor("#233238"))

            val color = ContextCompat.getColor(holder.itemView.context, R.color.myWhite)
            holder.ivFlightType.setColorFilter(color)

        }

    }

}