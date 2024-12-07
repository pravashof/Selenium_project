export const getLocalStorage = () => {
    return localStorage.getItem("userData");
}

export const setLocalStorage = (username, role) => {
    jsonData = {
        "username": username,
        "role": role
    }
    localStorage.setItem("userData", JSON.stringify(jsonData))
}
// export default getLocalStorage, setLocalStorage