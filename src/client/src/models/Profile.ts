class Profile {
  public id: number;
  public username: string;
  public firstName: string;
  public lastName: string;
  public timestamp: Date;

  constructor() {
    this.id = 0;
    this.username =
        this.firstName =
        this.lastName = '';
    this.timestamp = new Date();
  }
}

export default Profile;
