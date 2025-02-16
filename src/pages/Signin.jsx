import React, { useEffect } from 'react'
import { GoogleLogin } from '@react-oauth/google';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';


function Signin() {
    const { user, handleLoginSuccess, handleLoginFailure } = useAuth(); 
    const navigate = useNavigate();



    /**
     * On mount + user change
     */
    useEffect(() => {
        if (user) {
            navigate("/");
        }
    }, [user])

    /**
     * Pass the credential to auth context
     * 
     * @param {*} credential 
     */
    const responseGoogle = async (credential) => { 
        if (credential){ 
            handleLoginSuccess(credential)
        } 
    } 

    

    const temp = () =>{ 
        fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/checksession`,{ 
            credentials: 'include' 
        }) 
        .then((response) => { 
            return response.json(); 
        }) 
        .then((myJson) => { 
            alert(myJson) 
        }); 
    } 



    return (
        <div id="sign-in" className="w-full h-screen flex items-center justify-center">
            <div className="w-[40%] flex flex-col gap-4 p-6 border-[1px] rounded-xl border-light-gray justify-center items-center">
                <p>No sensitive information will be shared</p>
                <GoogleLogin
                    onSuccess={credentialResponse => {
                        responseGoogle(credentialResponse.credential);
                    }}
                    onError={() => {
                        handleLoginFailure();
                    }}
                    width={200}
                    shape='pill'
                />
                <button onClick={temp}> Check session </button> 
            </div>
        </div>
    )
}

export default Signin;