
const apiHost = "localhost";
//const apiHost = "api.moneyprintergobrr.io";
//const apiHost = "development.eba-jgr836tj.us-west-2.elasticbeanstalk.com";

const Env = {
  API_HOST: process.env.MP_API_HOST ?? apiHost,
  API_VERSION: "v1",
  DEBUG: true
};

export default Env;