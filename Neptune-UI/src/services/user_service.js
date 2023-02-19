const API_URL = '/api/v2/user'

class UserService {
    getUserData() {
        return axios.get(API_URL, { headers: authHeader(),  });
    }
}

export default new UserService();