import { GeneratorValues, ProjectDataRow } from '../types'

export const generateSubject = (
  project: GeneratorValues | undefined,
  webmaster: GeneratorValues | undefined,
  website: GeneratorValues | undefined
): string => {
  return `Ads for - ${website?.name}`
}

export const generateBody = (
  project: GeneratorValues | undefined,
  website: GeneratorValues | undefined,
  projectsData: ProjectDataRow | undefined | null
): string => {
  if (!project || !website) {
    return ''
  }

  const foundProject = projectsData.find((item) => item.id === project.id)

  if (!foundProject || !foundProject.url) {
    return ''
  }

  const { url } = foundProject.url

  const responses = [
    `Hello! Could you please tell me what conditions exist for publishing project material ${url} on your resource - ${website?.name}.`,
    `Greetings! I'm interested in understanding the publishing conditions for project material ${url} on your site, particularly regarding ${website?.name}.`,
    `Hi there! I'd like to know more about how project content from ${url} is published on your website - specifically related to ${website?.name}.`,
    `Hello! We're curious about the publishing guidelines for project content ${url} on your platform, especially for ${website?.name}.`,
    `Greetings! We're looking to learn more about the publication requirements for project material ${url} on your site, particularly for ${website?.name}.`,
    `Hi there! Could you provide insights into the procedures for publishing content from project ${url} on your website, specifically regarding ${website?.name}.`,
    `Hello! We're interested in the publication conditions for project content ${url} on your site, especially for ${website?.name}.`,
    `Greetings! We'd like to understand how project material from ${url} is typically published on your platform, particularly for ${website?.name}.`,
    `Hi there! We're looking to gather information on the publishing policies for project content ${url} on your site, particularly for ${website?.name}.`
  ]

  const randomResponse =
    responses[Math.floor(Math.random() * responses.length)]

  return randomResponse
}
