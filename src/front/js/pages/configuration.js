import React, { useState, useEffect, useContext } from "react";
import { Link, useParams, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";

// import "/workspaces/Watacar_v2/src/front/styles/configuration.css"
// import "/workspaces/Watacar_v2/src/front/styles/profile.css"
import "../../styles/configuration.css"
import "../../styles/profile.css"

import { text } from "@fortawesome/fontawesome-svg-core";
import { Placeholder_profile } from "./placeholder_profile.js"
export const Configuration = () => {
    const {actions, store} = useContext(Context);
    const [data, setData] = useState([]);
    const [showFileInput, setShowFileInput] = useState(false); 

    const navigate =useNavigate();
useEffect (() => {
    actions.getUser();
}, [])
const handleChange = (e) => {
        setData({ ...data, [e.target.name]: e.target.value });
        //console.log(data);
}
useEffect(() => {
    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyAf7aQ5JHWwJTvYuzpJw8QtQK8DYdwJqPE&libraries=places`;
    script.async = true;
    script.onload = handleScriptLoad;
    document.body.appendChild(script);
    return () => {
      document.body.removeChild(script);
    };
  }, []);
  const handleScriptLoad = () => {
    const input = document.getElementById("address");
    const autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.addListener("place_changed", () => {
      const selectedPlace = autocomplete.getPlace();
      const address = selectedPlace.formatted_address;
      setData({ ...data, adress: address });
    });
  };
const handleSubmit = (event) => {
    event.preventDefault()
    const updatedData = {
        ...store.user,
        ...data,
      };
    const putConfig = {
        method: "PUT",
        body: JSON.stringify({
            "address": updatedData.adress,
            "email": updatedData.email,
            "document_type": updatedData.document_type,
            "document_number": updatedData.document_number,
            "full_name": updatedData.full_name,
            "phone": updatedData.phone,
            avatar: updatedData.avatar,
        }),
        headers: {
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
    }
    fetch(process.env.BACKEND_URL + "api/configuration", putConfig)
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      throw new Error("Error al guardar los datos");
    })
    .then((responseData) => {
      setData({ ...data, response: responseData });
      Swal.fire({
        icon: 'success',
        title: 'Datos actualizados',
      });
      navigate("/profile/configuration");
    })
    .catch((error) => {
      console.error(error);
    });
};

const handleAvatar = async (e) => {
  const file = e.target.files[0]
  if (!file) return ;

  const formData = new FormData()
  formData.append("file", file);
  formData.append("upload_preset", "WhataCar");
  formData.append("api_key", process.env.API_KEY);
  formData.append("timestamp", Math.floor(Date.now() / 1000));


  
  // return fetch(
  //     "https://api.cloudinary.com/v1_1/djpzj47gu/image/upload",
  //     {
  //       method: "POST",
  //       body: formData,
  //     }
  //   )
  //   .then((resp) => resp.json())
  //   .then((data) => {
  //     console.log("Avatar updated", data)
  //     return avatar= data.secure_url
  //   })

  try {
    const response = await fetch(
      "https://api.cloudinary.com/v1_1/djpzj47gu/image/upload",
      {
        method: "POST",
        body: formData,
      }
    );
    const data = await response.json();

    setData((prevData) => ({
      ...prevData,
      avatar: data.secure_url,
    }));
  } catch (error) {
    console.error("Error uploading avatar:", error);
  }
};


return store.user ? (
  <div className="container_profile">
        <div className="mx-5 px-5 box w-100">
        <div className="d-lg-flex justify-content-start my-5">
        <div className="avatar_container">
          {console.log(store.user.avatar)}
          <img
            className="avatar_image"
            src={store.user.avatar  || "https://www.fundaciocaixaltea.com/wp-content/uploads/2018/01/default-profile.png"}
            // src={store.user.avatar !== null ?  store.user.avatar : "https:/c/appsdejoseluis.com/wp-content/uploads/2020/04/face_co.png"}
            // src={store.user.avatar || "https://appsdejoseluis.com/wp-content/uploads/2020/04/face_co.png"}

            alt="Avatar"
          />
        </div>
        <button className="btn_pencil_avatar" onClick={() => setShowFileInput(true)}>✏️</button>
          {showFileInput && ( // Mostrar el input solo si showFileInput es true
            <input className="profileimginput" type="file" onChange={handleAvatar} placeholder="Elije la foto"></input>
          )}
        </div>

        <div className="profile_info m-auto pb-5">
          <div className="row_profile_configuration">
                        <label className=" text-wrap badge label col-sm-10 col-md-6 col-lg-8 m-3">Nombre:</label>
                        <input className="user_data inputProfile col-sm-4 col-md-6 col-lg-8 ms-5 mb-3" name="full_name" type="text" value={data.full_name || store.user.full_name} onChange={handleChange}></input>
                    </div>
                    <div className="row_profile_configuration">
                        <label className=" text-wrap badge label  col-sm-10 col-md-6 col-lg-8 mb-3">Email:</label>
                        <input className="user_data inputProfile  col-sm-10 col-md-6 col-lg-8 ms-5 mb-3" name="email" type="text" value={data.email || store.user.email} onChange={handleChange}></input>
                    </div>
                    <div className="row_profile_configuration">
                      <label className=" text-wrap badge label col-sm-12 col-md-6 col-lg-8 mb-3">Tipo de documento:</label>
                      <select className="user_data inputProfile  col-sm-10 col-md-6 col-lg-8 ms-5 mb-3" name="document_type" value={data.document_type || store.user.document_type} onChange={handleChange}>
                        <option value="DNI">DNI</option>
                        <option value="CIF">CIF</option>
                      </select>
                    </div>
                        <div className="row_profile_configuration">
                            <label className=" text-wrap badge label  col-sm-10 col-md-6 col-lg-8 mb-3">Número del documento:</label>
                            <input className="user_data inputProfile col-sm-10 col-md-6 col-lg-8 ms-5" name="document_number" type="text" value={data.document_number || store.user.document_number} onChange={handleChange}></input>
                        </div>
                        <div className="row_profile_configuration">
                        <label className=" text-wrap badge label  col-sm-12 col-md-6 col-lg-8 mb-3">Teléfono:</label>
                        <input className="user_data inputProfile col-sm-10 col-md-6 col-lg-8 ms-5 mb-3" name="phone" type="text" value={data.phone || store.user.phone} onChange={handleChange}></input>
                    </div>
                    <div className="row_profile_configuration">
                    <label className=" text-wrap badge label col-sm-12 col-md-6 col-lg-8 mb-3">Dirección:</label>
                        <input className="user_data inputProfile col-sm-10 col-md-6 col-lg-8 ms-5 mb-3" id="address" name="adress" type="text" value={data.adress || store.user.address} onChange={handleChange}></input>
                    </div>
                    <div className=" save_cancel_config">
                        <Link to="/profile/configuration" className="btn_config cancel">
                            Cancelar
                        </Link>
                        <Link to="/profile/configuration" className="btn_config save" onClick={handleSubmit}>
                            Guardar
                        </Link>
                    </div>
                    </div>
                    </div>
                </div>
): <div className="spinner-border text-primary m-auto d-flex
justify-content-center "
style={{"width": "10rem", "height": "10rem"}}
role="status">
</div>
}

















