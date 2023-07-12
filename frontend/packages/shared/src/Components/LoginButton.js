import { useEffect, useState } from "react"
import { Navigate, useSearchParams } from "react-router-dom"

import jwt_decode from "jwt-decode";


export const LoginPage = (props) => {
    let [searchParams, setSearchParams] = useSearchParams();
    const [token, setToken] = useState(null)
    const [user, setuser] = useState(null)

    const code = searchParams.get("code")
    const whereToAsk = "http://localhost:8000/oauth/token"
    useEffect(() => {
        // if (false) {
        if (token) {
            if (user) {

            } else {
                console.log("unknown user, asking with", token)
                const whereToAsk = "http://localhost:8000/oauth/userinfo"
                console.log("using token", token.access_token)
                fetch(whereToAsk, {
                    method: 'GET',
                    headers: {
                        'mode': 'cors',
                        'authorization': 'Bearer ' + token.access_token
                    }
                })
                .then(
                    response => response.text()
                )
                .then(
                    code => {
                        const decoded = jwt_decode(code);
                        console.log("got user", decoded)
                    }
                )
            }
        } else {
            console.log('have not a token')
            if (code) {
                console.log('have code', code)
                const formData = {
                    code: code,
                    grant_type: "authorization_code"
                }

                let formBody = [];
                for (var property in formData) {
                    var encodedKey = encodeURIComponent(property);
                    var encodedValue = encodeURIComponent(formData[property]);
                    formBody.push(encodedKey + "=" + encodedValue);
                }
                formBody = formBody.join("&");

                fetch(whereToAsk, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                        'mode': 'cors'
                    },
                    body: formBody
                })
                .then(
                    response => response.text()
                )
                .then(
                    text => {
                        console.log("got token", text)
                        const decoded = jwt_decode(text);
                        console.log("decode token", decoded)
                        localStorage.setItem("token", decoded);
                        
                        setToken(decoded)
                    }
                )
            }
        }

        //const token = localStorage.getItem("token")
        
    })
    return (
        <>
        LOGIN PAGE
        {/* {JSON.stringify(props)}<br /> */}
        {JSON.stringify(searchParams)}<br />
        {JSON.stringify(searchParams.get("code"))}<br />
        {JSON.stringify(searchParams.get("state"))}<br />
        {JSON.stringify(Object.keys(searchParams))}<br />
        <LoginButton />
        </>
    )
}

export const LoginButton = ({oauthurl = "http://localhost:8000/oauth/login?redirect_uri=http://localhost:3000/ui/login"}) => {
    const loginClicked = () => {
        window.location.assign(oauthurl)
    }
    const cat = localStorage.getItem("token");

    return (
        <button className="btn btn-outline-primary" onClick={loginClicked}>Přihlásit</button>
    )
}