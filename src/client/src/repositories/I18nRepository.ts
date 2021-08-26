import i18next from "i18next";

import en from "../i18n/en.json"

class I18nRepository {

  constructor(lang='en') {
    i18next.init({
      lng: lang,
      debug: false,
      resources: this.constructLangs()
    })
  }

  public t = i18next.t;

  private constructLangs() {
    return en;
  }

}

export default I18nRepository;
