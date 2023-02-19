export function getprettytimestamp (datestring = Date.now().toString()){
    let dateobject = new Date(datestring)
    return dateobject.toLocaleDateString()+ " " +  dateobject.toLocaleTimeString()
}

export default function authHeader() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && user.accessToken) {
      return { Authorization: 'Bearer ' + user.accessToken };
    } else {
      return {};
    }
  }