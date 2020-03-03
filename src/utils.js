export function getprettytimestamp (datestring = Date.now().toString()){
    let dateobject = new Date(datestring)
    return dateobject.toLocaleDateString()+ " " +  dateobject.toLocaleTimeString()
}