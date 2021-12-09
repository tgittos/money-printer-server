export interface IAuthedProfile {
  profile: IProfile
  token: string
}

export interface IProfile {
  id: number | null;
  username: string;
  email?: string;
  firstName: string;
  first_name?: string;
  lastName: string;
  last_name?: string;
  timestamp: Date;
  is_admin?: boolean;
  isAdmin: boolean;
}

class Profile implements IProfile {
  public id: number | null;
  public username: string;
  public firstName: string;
  public lastName: string;
  public timestamp: Date;
  public isAdmin: boolean;

  constructor(obj: IProfile) {
    this.id = obj?.id ?? null;
    this.username = obj?.email ?? '';
    this.firstName = obj?.first_name ?? '';
    this.lastName = obj?.last_name ?? '';
    this.timestamp = obj?.timestamp ?? new Date();
    this.isAdmin = obj?.is_admin ?? false;
  }
}

export default Profile;
