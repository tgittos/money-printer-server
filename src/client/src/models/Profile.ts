class Profile {
  public username: string;
  public firstName: string;
  public lastName: string;
  public authenticated: boolean;

  constructor() {
    this.username =
        this.firstName =
        this.lastName = '';
    this.authenticated = false;
  }
}

export default Profile;
