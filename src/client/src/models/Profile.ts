interface IServerProfile {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  timestamp: Date;
}

class Profile {
  public id: number;
  public username: string;
  public firstName: string;
  public lastName: string;
  public timestamp: Date;

  constructor(obj: IServerProfile = {} as IServerProfile) {
    this.id = obj?.id ?? 0;
    this.username = obj?.email ?? '';
    this.firstName = obj?.first_name ?? '';
    this.lastName = obj?.last_name ?? '';
    this.timestamp = obj?.timestamp ?? new Date();
  }
}

export default Profile;
