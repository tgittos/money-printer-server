class Profile {
  public username: string;
  public firstName: string;
  public lastName: string;
  public authenticated: boolean;
  public timestamp: Date;

  constructor() {
    this.username =
        this.firstName =
        this.lastName = '';
    this.authenticated = false;
  }
}

export default Profile;
