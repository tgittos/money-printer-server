import i18next from "i18next";

import Env from "../env";
import en from "../i18n/en.json"

class I18nRepository {

  constructor(lang='en') {
    i18next.init({
      lng: lang,
      debug: false,
      resources: this.constructLangs()
    });

    if (Env.DEBUG) {
      console.log('I18nRepository:constructor - loaded language file:', i18next.t('register_login'));
    }
  }

  public t(key, obj) {
    return i18next.t(key, obj);
  }

  private constructLangs() {
    return en;
  }

}

export default I18nRepository;
