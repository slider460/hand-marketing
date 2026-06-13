import { youtubeEmbed, VideoItem } from '../lib/content'

export default function VideoEmbed({ video }: { video: VideoItem }) {
  const yt = youtubeEmbed(video.src)
  if (yt) {
    return (
      <div className="aspect-video w-full overflow-hidden rounded-2xl bg-black">
        <iframe
          src={yt}
          title="Видео"
          className="h-full w-full"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          loading="lazy"
        />
      </div>
    )
  }
  // mp4 (в т.ч. dropbox) — нативный плеер
  const src = video.src.replace('www.dropbox.com', 'dl.dropboxusercontent.com').replace('?dl=0', '')
  return (
    <video controls preload="metadata" className="aspect-video w-full rounded-2xl bg-black">
      <source src={src} type="video/mp4" />
    </video>
  )
}
