import i18next from "i18next";

import Env from "../env";
import en from "../i18n/en.json"

class I18nService {

  constructor(lang='en') {
    i18next.init({
      lng: lang,
      debug: false,
      resources: this.constructLangs()
    });

    if (Env.DEBUG) {
      console.log('I18nRepository:constructor - loaded language file', lang);
    }
  }

  public t(key: string, obj: any = {}) {
    return i18next.t(key, obj);
  }

  private constructLangs() {
    return en;
  }

}

export default I18nService;
