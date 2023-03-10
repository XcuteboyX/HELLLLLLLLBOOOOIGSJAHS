import time

import requests
from bs4 import BeautifulSoup
from TelethonHell.helpers.pasters import telegraph_paste

ANIME_DB = {}
MANGA_DB = {}
CHARC_DB = {}
FILLERS_ = {}


# Template for anime queries
ANIME_TEMPLATE = """{name}
โโโโ๐โโโโ
**ยป ID :** `{idm}`
**ยป MAL ID :** `{idmal}`
โโโโ๐โโโโ
**โ SOURCE :**  `{source}`
**โ TYPE :**  `{formats}`{avscd}{dura}
**โ ADULT RATED :**  `{adult}`
{status_air}{gnrs_}{tags_}
**โ TRAILER :** {trailer_link}
**โ WEBSITE :** [{english}]({url})
**โ SYNOPSIS :** [Description]({paste})

{additional}

        **<\>** {chnl}
"""

# Basically gives data of searched anime based on anilist pages.
PAGE_QUERY = """
query ($search: String, $page: Int) {
  Page (perPage: 1, page: $page) {
    pageInfo {
      total
    }
    media (search: $search, type: ANIME) {
      id
      idMal
      title {
        romaji
        english
        native
      }
      format
      status
      episodes
      duration
      countryOfOrigin
      description (asHtml: false)
      source (version: 2)
      trailer {
        id
        site
      }
      genres
      tags {
        name
      }
      averageScore
      relations {
        edges {
          node {
            title {
              romaji
              english
            }
          }
          relationType
          }
        }
      nextAiringEpisode {
        timeUntilAiring
        episode
      }
      isAdult
      mediaListEntry {
        status
        score
        id
      }
      siteUrl
    }
  }
}
"""

# returns manga details in json
MANGA_QUERY = """
query ($search: String, $page: Int) {
  Page (perPage: 1, page: $page) {
    pageInfo {
      total
    }
    media (search: $search, type: MANGA) {
      id
      title {
        romaji
        english
        native
      }
      format
      countryOfOrigin
      source (version: 2)
      status
      description(asHtml: true)
      chapters
      mediaListEntry {
        status
        score
        id
      }
      volumes
      averageScore
      siteUrl
      isAdult
    }
  }
}
"""

# returns character data in json
CHARACTER_QUERY = """
query ($id: Int, $search: String, $page: Int) {
  Page (perPage: 1, page: $page) {
    pageInfo{
      total
    }
    characters (id: $id, search: $search) {
      id
      name {
        full
        native
      }
      image {
        large
      }
      description(asHtml: true)
      siteUrl
      }
    }
  }
"""

# Airing Query from anilist
AIR_QUERY = """
query ($id: Int, $idMal:Int, $search: String) {
  Media (id: $id, idMal: $idMal, search: $search, type: ANIME) {
    id
    title {
      romaji
      english
    }
    status
    countryOfOrigin
    nextAiringEpisode {
      timeUntilAiring
      episode
    }
    siteUrl
    isFavourite
    mediaListEntry {
      status
      id
    }
  }
}
"""

# returns user data from anilist

USER_QRY = """
query ($search: String) {
  User (name: $search) {
    id
    name
    siteUrl
    statistics {
      anime {
        count
        minutesWatched
        episodesWatched
        meanScore
      }
      manga {
        count
        chaptersRead
        volumesRead
        meanScore
      }
    }
  }
}
"""


# searches for fillers episodes
def search_filler(query):
    html = requests.get("https://www.animefillerlist.com/shows").text
    soup = BeautifulSoup(html, "html.parser")
    div = soup.findAll("div", attrs={"class": "Group"})
    index = {}
    for i in div:
        li = i.findAll("li")
        for jk in li:
            yum = jk.a["href"].split("/")[-1]
            cum = jk.text
            index[cum] = yum
    ret = {}
    keys = list(index.keys())
    for i in range(len(keys)):
        if query.lower() in keys[i].lower():
            ret[keys[i]] = index[keys[i]]
    return ret


# parse the searched filler episodes
def parse_filler(filler_id):
    url = "https://www.animefillerlist.com/shows/" + filler_id
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", attrs={"id": "Condensed"})
    all_ep = div.find_all("span", attrs={"class": "Episodes"})
    if len(all_ep) == 1:
        ttl_ep = all_ep[0].findAll("a")
        total_ep = []
        mix_ep = None
        filler_ep = None
        ac_ep = None
        for tol in ttl_ep:
            total_ep.append(tol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": mix_ep,
            "filler_ep": filler_ep,
            "ac_ep": ac_ep,
        }
        return dict_
    if len(all_ep) == 2:
        ttl_ep = all_ep[0].findAll("a")
        fl_ep = all_ep[1].findAll("a")
        total_ep = []
        mix_ep = None
        ac_ep = None
        filler_ep = []
        for tol in ttl_ep:
            total_ep.append(tol.text)
        for fol in fl_ep:
            filler_ep.append(fol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": mix_ep,
            "filler_ep": ", ".join(filler_ep),
            "ac_ep": ac_ep,
        }
        return dict_
    if len(all_ep) == 3:
        ttl_ep = all_ep[0].findAll("a")
        mxl_ep = all_ep[1].findAll("a")
        fl_ep = all_ep[2].findAll("a")
        total_ep = []
        mix_ep = []
        filler_ep = []
        ac_ep = None
        for tol in ttl_ep:
            total_ep.append(tol.text)
        for fol in fl_ep:
            filler_ep.append(fol.text)
        for mol in mxl_ep:
            mix_ep.append(mol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": ", ".join(mix_ep),
            "filler_ep": ", ".join(filler_ep),
            "ac_ep": ac_ep,
        }
        return dict_
    if len(all_ep) == 4:
        ttl_ep = all_ep[0].findAll("a")
        mxl_ep = all_ep[1].findAll("a")
        fl_ep = all_ep[2].findAll("a")
        al_ep = all_ep[3].findAll("a")
        total_ep = []
        mix_ep = []
        filler_ep = []
        ac_ep = []
        for tol in ttl_ep:
            total_ep.append(tol.text)
        for fol in fl_ep:
            filler_ep.append(fol.text)
        for mol in mxl_ep:
            mix_ep.append(mol.text)
        for aol in al_ep:
            ac_ep.append(aol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": ", ".join(mix_ep),
            "filler_ep": ", ".join(filler_ep),
            "ac_ep": ", ".join(ac_ep),
        }
        return dict_


# Gets country of origin
def cflag(country):
    if country == "JP":
        return "\U0001F1EF\U0001F1F5"
    if country == "CN":
        return "\U0001F1E8\U0001F1F3"
    if country == "KR":
        return "\U0001F1F0\U0001F1F7"
    if country == "TW":
        return "\U0001F1F9\U0001F1FC"


# Position format for airing
def pos_no(no):
    ep_ = list(str(no))
    x = ep_.pop()
    if ep_ != [] and ep_.pop() == "1":
        return "th"
    th = "st" if x == "1" else "nd" if x == "2" else "rd" if x == "3" else "th"
    return th


# time stamp for airing
def make_it_rw(time_stamp):
    seconds, milliseconds = divmod(int(time_stamp), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " Days, ") if days else "")
        + ((str(hours) + " Hours, ") if hours else "")
        + ((str(minutes) + " Minutes, ") if minutes else "")
        + ((str(seconds) + " Seconds, ") if seconds else "")
        + ((str(milliseconds) + " ms, ") if milliseconds else "")
    )
    return tmp[:-2]


# returns data in json
async def return_json_senpai(query: str, vars_: dict):
    url = "https://graphql.anilist.co"
    return requests.post(url, json={"query": query, "variables": vars_}).json()


# gets anime details from anilist
async def get_anilist(qdb, page):
    vars_ = {"search": ANIME_DB[qdb], "page": page}
    result = await return_json_senpai(PAGE_QUERY, vars_)
    if len(result["data"]["Page"]["media"]) == 0:
        return [f"No results Found"]
    data = result["data"]["Page"]["media"][0]
    # pylint: disable=possibly-unused-variable
    chnl = "[โ?hรช Hรชllแบรธโ?](https://t.me/Its_Hellbot)"
    idm = data.get("id")
    idmal = data.get("idMal")
    romaji = data["title"]["romaji"]
    english = data["title"]["english"]
    native = data["title"]["native"]
    formats = data.get("format")
    status = data.get("status")
    episodes = data.get("episodes")
    duration = data.get("duration")
    country = data.get("countryOfOrigin")
    c_flag = cflag(country)
    source = data.get("source")
    prqlsql = data.get("relations").get("edges")
    adult = data.get("isAdult")
    trailer_link = "N/A"
    gnrs = ", ".join(data["genres"])
    gnrs_ = ""
    if len(gnrs) != 0:
        gnrs_ = f"\n**โ GENRES :**  `{gnrs}`"
    score = data["averageScore"]
    avscd = f"\n**โ SCORE :**  `{score}%` ๐" if score is not None else ""
    tags = []
    for i in data["tags"]:
        tags.append(i["name"])
    tags_ = f"\n**โ TAGS :** `{', '.join(tags[:5])}`" if tags != [] else ""
    in_ls = False
    in_ls_id = ""
    if data["title"]["english"] is not None:
        name = f"ยซ {c_flag} ยป **{english}** (`{native}`)"
    else:
        name = f"ยซ {c_flag} ยป **{romaji}** (`{native}`)"
    prql, sql = "", ""
    for i in prqlsql:
        if i["relationType"] == "PREQUEL":
            pname = (
                i["node"]["title"]["english"]
                if i["node"]["title"]["english"] is not None
                else i["node"]["title"]["romaji"]
            )
            prql += f"**โข PREQUEL :** `{pname}`\n"
            break
    for i in prqlsql:
        if i["relationType"] == "SEQUEL":
            sname = (
                i["node"]["title"]["english"]
                if i["node"]["title"]["english"] is not None
                else i["node"]["title"]["romaji"]
            )
            sql += f"**โข SEQUEL :** `{sname}`\n"
            break
    additional = f"{prql}{sql}"
    additional.replace("-", "")
    dura = f"\n**โ DURATION :** `{duration} min/ep`" if duration is not None else ""
    air_on = None
    if data["nextAiringEpisode"]:
        nextAir = data["nextAiringEpisode"]["timeUntilAiring"]
        air_on = make_it_rw(nextAir * 1000)
        eps = data["nextAiringEpisode"]["episode"]
        th = pos_no(str(eps))
        air_on += f" | {eps}{th} eps"
    if air_on is None:
        eps_ = f"` | `{episodes} eps" if episodes is not None else ""
        status_air = f"**โ STATUS :** `{status}{eps_}`"
    else:
        status_air = f"**โ STATUS :** `{status}`\n**โ NEXT AIRING :** `{air_on}`"
    if data["trailer"] and data["trailer"]["site"] == "youtube":
        trailer_link = f"[YouTube](https://youtu.be/{data['trailer']['id']})"
    url = data.get("siteUrl")
    banner = f"https://img.anili.st/media/{idm}"
    banner_ = requests.get(banner)
    open(f"{idm}.jpg", "wb").write(banner_.content)
    title_img = f"{idm}.jpg"
    logo = "https://telegra.ph/file/2c546060b20dfd7c1ff2d.jpg"
    descr = ""
    descr += f"<img src='{banner}'/> \n"
    descr += data["description"]
    descr += f"\n\n<img src='{logo}' />"
    paste = await telegraph_paste(f"Description For โ {english} โ", descr)
    total = result["data"]["Page"]["pageInfo"]["total"]
    try:
        finals_ = ANIME_TEMPLATE.format(**locals())
    except KeyError as kys:
        return [f"{kys}"]
    return title_img, [finals_], [idm, in_ls, in_ls_id, str(adult)]


# parse manga details
async def get_manga(qdb, page):
    vars_ = {"search": MANGA_DB[qdb], "asHtml": True, "page": page}
    result = await return_json_senpai(MANGA_QUERY, vars_)
    if len(result["data"]["Page"]["media"]) == 0:
        return [f"No results Found"]
    data = result["data"]["Page"]["media"][0]
    # Data of all fields in returned json
    # pylint: disable=possibly-unused-variable
    idm = data.get("id")
    romaji = data["title"]["romaji"]
    english = data["title"]["english"]
    native = data["title"]["native"]
    status = data.get("status")
    synopsis = data.get("description")
    volumes = data.get("volumes")
    chapters = data.get("chapters")
    score = data.get("averageScore")
    url = data.get("siteUrl")
    format_ = data.get("format")
    country = data.get("countryOfOrigin")
    source = data.get("source")
    c_flag = cflag(country)
    adult = data.get("isAdult")
    in_ls = False
    in_ls_id = ""
    name = f"""ยซ {c_flag} ยป {romaji}
     **โน {english} โบ** 
      `{native}` """
    if english is None:
        name = f"""ยซ {c_flag} ยป **{romaji}**
        {native}"""
    banner = f"https://img.anili.st/media/{idm}"
    logo = "https://telegra.ph/file/2c546060b20dfd7c1ff2d.jpg"
    descr = ""
    descr += f"<img src='{banner}'/> \n"
    descr += synopsis
    descr += f"\n\n<img src='{logo}' />"
    paste = await telegraph_paste(f"Description For โ {romaji} โ", descr)
    finals_ = f"{name}\n\n"
    finals_ += f"**โ ID :** `{idm}`\n"
    finals_ += f"**โ STATUS :** `{status}`\n"
    finals_ += f"**โ VOLUMES :** `{volumes}`\n"
    finals_ += f"**โ CHAPTERS :** `{chapters}`\n"
    finals_ += f"**โ SCORE :** `{score}`\n"
    finals_ += f"**โ FORMAT :** `{format_}`\n"
    finals_ += f"**โ SOURCE :** `{source}`\n"
    finals_ += f"**โ DESCRIPTION :** [Synopsis]({paste})\n\n"
    finals_ += f"\n       **<\>** [โ?hรช Hรชllแบรธโ?](https://t.me/its_hellbot)"
    banner_ = requests.get(banner)
    open(f"{idm}.jpg", "wb").write(banner_.content)
    pic = f"{idm}.jpg"
    return (
        pic,
        [finals_, result["data"]["Page"]["pageInfo"]["total"], url],
        [idm, in_ls, in_ls_id, str(adult)],
    )


# parse character details.
async def get_character(query, page):
    var = {"search": CHARC_DB[query], "page": int(page)}
    result = await return_json_senpai(CHARACTER_QUERY, var)
    if len(result["data"]["Page"]["characters"]) == 0:
        return [f"No results Found"]
    data = result["data"]["Page"]["characters"][0]
    # Character Data
    id_ = data["id"]
    name = data["name"]["full"]
    native = data["name"]["native"]
    img = data["image"]["large"]
    site_url = data["siteUrl"]
    desc = data["description"]
    logo = "https://telegra.ph/file/2c546060b20dfd7c1ff2d.jpg"
    descr = ""
    descr += f"<img src='{img}'/> \n"
    descr += desc
    descr += f"\n\n<img src='{logo}' />"
    paste = await telegraph_paste(f"More Info For โ {name} โ", descr)
    cap_text = f"""
**โ CHARACTER :** `{name}` 
        โน `{native}` โบ
**โ ID :** `{id_}`
**โ WEBSITE :** [{name}]({site_url})
**โ DETAILS :** [More Info...]({paste})


        **<\>** [โ?hรช Hรชllแบรธโ?](https://t.me/its_hellbot)
"""
    total = result["data"]["Page"]["pageInfo"]["total"]
    return img, [cap_text, total], [id_]


# finally formats all the data and gives airing info
async def get_airing(vars_):
    result = await return_json_senpai(AIR_QUERY, vars_)
    error = result.get("errors")
    if error:
        error_sts = error[0].get("message")
        return [f"{error_sts}"]
    data = result["data"]["Media"]
    mid = data.get("id")
    romaji = data["title"]["romaji"]
    english = data["title"]["english"]
    status = data.get("status")
    country = data.get("countryOfOrigin")
    c_flag = cflag(country)
    banner = f"https://img.anili.st/media/{mid}"
    banner_ = requests.get(banner)
    open(f"{mid}.jpg", "wb").write(banner_.content)
    coverImg = f"{mid}.jpg"
    in_ls = False
    in_ls_id = ""
    air_on = None
    if data["nextAiringEpisode"]:
        nextAir = data["nextAiringEpisode"]["timeUntilAiring"]
        episode = data["nextAiringEpisode"]["episode"]
        th = pos_no(episode)
        air_on = make_it_rw(nextAir * 1000)
    title_ = english or romaji
    out = f"[{c_flag}] **{title_}**"
    out += f"\n**โช ID :** `{mid}`"
    out += f"\n**โช Status :** `{status}`\n"
    if air_on:
        out += f"\n**โช Airing Episode** `{episode}{th}` **in** `{air_on}`"
    site = data["siteUrl"]
    return [coverImg, out], site, [mid, in_ls, in_ls_id]


async def get_user(vars_):
    query = USER_QRY
    k = await return_json_senpai(query=query, vars_=vars_)
    error = k.get("errors")
    if error:
        error_sts = error[0].get("message")
        return [f"{error_sts}"]

    data = k["data"]["User"]
    xid = data["id"]
    banner = f'https://img.anili.st/user/{data["id"]}?a={time.time()}'
    banner_ = requests.get(banner)
    open(f"{xid}.jpg", "wb").write(banner_.content)
    pic = f"{xid}.jpg"
    anime = data["statistics"]["anime"]
    manga = data["statistics"]["manga"]
    stats = f"""
<b><i>โช <u>Anime Stats</u> :<b><i>

<b><i>โ Animes Watched :</b></i> <i>{anime['count']}</i>
<b><i>โ Episodes Watched :</b></i> <i>{anime['episodesWatched']}</i>
<b><i>โ Time Spent :</b></i> <i>{anime['minutesWatched']}</i>
<b><i>โ Average Score :</b></i> <i>{anime['meanScore']}</i>


<b><i>โช <u>Manga Stats</u> :</b></i>

<b><i>โ Total Manga Read :</b> {manga['count']}</i>
<b><i>โ Total Chapters Read :</b> {manga['chaptersRead']}</i>
<b><i>โ Total Volumes Read :</b> {manga['volumesRead']}</i>
<b><i>โ Average Score :</b> {manga['meanScore']}</i>
"""
    return pic, stats
